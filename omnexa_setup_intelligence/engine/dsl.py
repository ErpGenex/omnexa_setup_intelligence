# Copyright (c) 2026, Omnexa and contributors
# License: MIT. See license.txt

from __future__ import annotations

import re


_TOKEN_RE = re.compile(r"\s+")


class DSLError(ValueError):
	pass


def _get_fact(facts: dict, path: str):
	cur = facts
	for part in path.split("."):
		if isinstance(cur, dict) and part in cur:
			cur = cur[part]
		else:
			return None
	return cur


def eval_condition(condition: str, facts: dict) -> bool:
	"""Evaluate a minimal, safe condition DSL.

	Supported:
	- <fact_path> == <number|string>
	- <fact_path> != <number|string>
	- <fact_path> >, >=, <, <= <number>
	- <fact_path> is empty | is not empty
	- combine with: AND / OR (left-to-right, no parentheses)
	"""
	cond = (condition or "").strip()
	if not cond:
		raise DSLError("Empty condition")

	# Normalize spaces + lowercase keywords while preserving quoted strings
	parts = _TOKEN_RE.split(cond)
	# simple parsing with AND/OR operators
	result = None
	op = None
	i = 0
	while i < len(parts):
		if parts[i].lower() in ("and", "or"):
			op = parts[i].lower()
			i += 1
			continue

		# Parse expression starting at i
		left = parts[i]
		if i + 1 >= len(parts):
			raise DSLError(f"Incomplete expression near: {left}")
		oper = parts[i + 1].lower()

		if oper == "is":
			if i + 2 >= len(parts):
				raise DSLError("Expected 'empty' after 'is'")
			rest = " ".join(parts[i + 2 : i + 5]).lower()
			if rest.startswith("empty"):
				val = _get_fact(facts, left)
				expr = val is None or val == "" or val == 0 or val == [] or val == {}
				i += 3
			elif rest.startswith("not"):
				# is not empty
				val = _get_fact(facts, left)
				expr = not (val is None or val == "" or val == 0 or val == [] or val == {})
				i += 4
			else:
				raise DSLError("Only 'is empty' / 'is not empty' supported")
		else:
			if i + 2 >= len(parts):
				raise DSLError("Missing right-hand value")
			right_raw = parts[i + 2]
			right = right_raw
			if right_raw.isdigit():
				right = int(right_raw)
			val = _get_fact(facts, left)
			if oper in ("==", "!="):
				expr = (val == right) if oper == "==" else (val != right)
			elif oper in (">", ">=", "<", "<="):
				try:
					lv = float(val or 0)
					rv = float(right)
				except Exception:
					expr = False
				else:
					if oper == ">":
						expr = lv > rv
					elif oper == ">=":
						expr = lv >= rv
					elif oper == "<":
						expr = lv < rv
					else:
						expr = lv <= rv
			else:
				raise DSLError(f"Unsupported operator: {oper}")
			i += 3

		if result is None:
			result = bool(expr)
		else:
			if op == "and":
				result = bool(result and expr)
			elif op == "or":
				result = bool(result or expr)
			else:
				# default to AND when operator missing
				result = bool(result and expr)

		op = None

	return bool(result)

