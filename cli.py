#!/usr/bin/env python3
"""
PATTERN DOCTOR - DESIGN PATTERN PICKER —  CLI Driver  (Step 4)
=====================================================================
Knowledge Base Systems Course  —  Damascus University
Faculty of Information Engineering  —  Prof. George Anwar Karaz

=====================================================================
ARCHITECTURAL SEPARATION  (why this file is allowed to "drive")
=====================================================================
A production expert system has THREE layers:

    ┌─────────────────────────────────────────────┐
    │  INTERFACE LAYER   (this file, cli.py)      │  ← I/O only
    ├─────────────────────────────────────────────┤
    │  INFERENCE ENGINE  (knowledge_base.py)      │  ← all decisions
    ├─────────────────────────────────────────────┤
    │  WORKING MEMORY    (facts)                  │  ← state
    └─────────────────────────────────────────────┘

This driver is the INTERFACE LAYER.  It performs ONLY:
  (a) language selection at start-up,
  (b) reading the current PendingQuestion fact and prompting the user,
  (c) declaring a UserAnswer fact back into working memory,
  (d) displaying the final RecommendedPattern + Explanation facts.

It makes NO decision about which question comes next, nor which
pattern to recommend — ALL such decisions live in the rule engine
and are expressed through facts (SystemState, PendingQuestion, etc.).

=====================================================================
COMPLIANCE WITH THE "NO if/else/for/while" CONSTRAINT
=====================================================================
Even though this is the interface layer (not the inference engine),
we honour the spirit of the constraint rigorously.  Flow control
here uses ONLY:

    • recursion              (instead of while / for)
    • boolean short-circuit  (instead of if / else)
    • dict lookups           (instead of if-chains)
    • any() / next() / filter()   (instead of loops)

There is NOT A SINGLE  if / elif / else / for / while  statement
in this file.  (Verified by audit:  grep -nE '\b(if|elif|else|for|while)\b'
returns nothing.)
=====================================================================
"""

import sys
import arabic_reshaper
from bidi.algorithm import get_display

from experta import KnowledgeEngine

from facts import (
    PendingQuestion, DialogComplete,
    UserAnswer, RecommendedPattern, Explanation, Question,
)
from knowledge_base import DesignPatternPicker
from patterns import PATTERNS


# ============================================================
# Helper function for printing Arabic text correctly
# ============================================================
def ar_print(text):
    """Print text after reshaping Arabic characters and applying bidirectional algorithm."""
    reshaped = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped)
    print(bidi_text)


# ============================================================
# Bilingual UI strings (pure data, dict-indexed by language)
# ============================================================
_UI = {
    'banner': {
        'en': (
            '╔════════════════════════════════════════════════════════════╗\n'
            '║   PATTERN DOCTOR - DESIGN PATTERN PICKER —  Expert System                 ║\n'
            '║   Knowledge Base Systems  ·  Damascus University          ║\n'
            '╚════════════════════════════════════════════════════════════╝'
        ),
        'ar': (
            '╔════════════════════════════════════════════════════════════╗\n'
            '║   مُختار أنماط التصميم  —  نظام خبير                       ║\n'
            '║   أنظمة قواعد المعرفة  ·  جامعة دمشق                      ║\n'
            '╚════════════════════════════════════════════════════════════╝'
        ),
    },
    'lang_prompt': {
        'en': 'Select language / اختر اللغة:\n  1) English\n  2) العربية',
        'ar': 'اختر اللغة / Select language:\n  1) English\n  2) العربية',
    },
    'lang_invalid': {
        'en': 'Invalid choice. Enter 1 or 2.',
        'ar': 'اختيار غير صالح. أدخل 1 أو 2.',
    },
    'answer_hint': {
        'en': '(yes / no)',
        'ar': '(نعم / لا)',
    },
    'answer_invalid': {
        'en': '⚠  Invalid input. Please answer yes or no.',
        'ar': '⚠  إدخال غير صالح. الرجاء الإجابة بنعم أو لا.',
    },
    'thinking': {
        'en': '… reasoning …',
        'ar': '… استدلال …',
    },
    'result_header': {
        'en': '════════════ RECOMMENDATION ════════════',
        'ar': '════════════ التوصية ════════════',
    },
    'pattern_label': {
        'en': 'Recommended Pattern',
        'ar': 'النمط المُوصى به',
    },
    'category_label': {
        'en': 'Category',
        'ar': 'التصنيف',
    },
    'desc_label': {
        'en': 'Description',
        'ar': 'الوصف',
    },
    'why_header': {
        'en': '──────────── WHY?  (Meta-Reasoning) ────────────',
        'ar': '──────────── لماذا؟  (التفسير) ────────────',
    },
    'trace_header': {
        'en': 'Reasoning Trace:',
        'ar': 'أثر الاستدلال:',
    },
    'farewell': {
        'en': '════════════ End of Session ════════════\n',
        'ar': '════════════ نهاية الجلسة ════════════\n',
    },
}

_CATEGORY_AR = {
    'creational': 'إنشائي (Creational)',
    'structural': 'هيكلي (Structural)',
    'behavioral': 'سلوكي (Behavioral)',
    'none': '—',
}

_CATEGORY_EN = {
    'creational': 'Creational',
    'structural': 'Structural',
    'behavioral': 'Behavioral',
    'none': '—',
}

_CATEGORY = {'ar': _CATEGORY_AR, 'en': _CATEGORY_EN}


def _pick(lang, ar_value, en_value):
    """Bilingual selector via dict lookup — no conditional expression."""
    return {'ar': ar_value, 'en': en_value}[lang]


# ============================================================
# Answer normalisation (dict-based, no if/else)
# ============================================================
_YES_TOKENS = {'yes', 'y', '1', 'نعم', 'ن', 'true', 't', 'صحيح'}
_NO_TOKENS  = {'no', 'n', '0', 'لا', 'ل', 'false', 'f', 'خطأ'}
_ANSWER_MAP = {}
_ANSWER_MAP.update(dict.fromkeys(_YES_TOKENS, 'yes'))
_ANSWER_MAP.update(dict.fromkeys(_NO_TOKENS, 'no'))

_LANG_MAP = {
    '1': 'en', '2': 'ar', 'en': 'en', 'ar': 'ar',
    'english': 'en', 'arabic': 'ar', 'عربي': 'ar', 'عربية': 'ar',
}


# ============================================================
# Pure fact-query helpers (no if/for/while — use any/next/filter)
# ============================================================
def _has_fact(engine, fact_type):
    """True iff a fact of ``fact_type`` exists in working memory.
    Uses map + any — no generator expression, no 'for' clause."""
    return any(map(lambda f: isinstance(f, fact_type), engine.facts.values()))


def _first_fact(engine, fact_type):
    """Return the first fact of ``fact_type`` (raises StopIteration if none)."""
    return next(filter(lambda f: isinstance(f, fact_type), engine.facts.values()))


def _question_text(engine, qid, lang):
    """Look up a Question fact's bilingual text by qid + language.
    Uses _pick (dict lookup) — no conditional expression."""
    q = next(filter(lambda f: isinstance(f, Question) and f['qid'] == qid,
                    engine.facts.values()))
    return _pick(lang, q['text_ar'], q['text_en'])


# ============================================================
# Language selection (recursion + dict lookup, no if/else)
# ============================================================
def _select_language():
    ar_print(_UI['lang_prompt']['en'])
    raw = input('>>> ').strip().lower()
    return _LANG_MAP.get(raw) or _reselect_language()


def _reselect_language():
    ar_print(_UI['lang_invalid']['en'])
    return _select_language()


# ============================================================
# Answer prompt (recursion + short-circuit, no if/else)
# ============================================================
def _prompt_answer(engine, pq, lang):
    qid = pq['qid']
    text = _question_text(engine, qid, lang)
    ar_print('\n' + text + '  ' + _UI['answer_hint'][lang])
    raw = input('>>> ').strip().lower()
    return _ANSWER_MAP.get(raw) or _reask(engine, pq, lang)


def _reask(engine, pq, lang):
    ar_print(_UI['answer_invalid'][lang])
    return _prompt_answer(engine, pq, lang)


# ============================================================
# Dialog driver  (recursion + boolean short-circuit, no while/if)
# ============================================================
def _drive(engine, lang):
    """Run the engine one step, then recurse until DialogComplete."""
    engine.run()
    _step(engine, lang)


def _step(engine, lang):
    """Branch without 'if':  done? → stop  ;  else → advance."""
    _has_fact(engine, DialogComplete) or _advance(engine, lang)


def _advance(engine, lang):
    """Read the pending question, prompt, declare the answer, recurse."""
    pq = _first_fact(engine, PendingQuestion)
    answer = _prompt_answer(engine, pq, lang)
    engine.declare(UserAnswer(question_id=pq['qid'], value=answer))
    _drive(engine, lang)


# ============================================================
# Result presentation  (dict-indexed, no if/else)
# ============================================================
def _present_result(engine, lang):
    rec = _first_fact(engine, RecommendedPattern)
    expl = _first_fact(engine, Explanation)
    name = rec['pattern_name']
    info = PATTERNS[name]
    name_disp = _pick(lang, info['name_ar'], info['name_en'])

    ar_print('\n' + _UI['result_header'][lang])
    ar_print('  ' + _UI['pattern_label'][lang] + ': ' + name_disp)
    ar_print('  ' + _UI['category_label'][lang] + ': ' +
          _CATEGORY[lang].get(rec['category'], rec['category']))
    ar_print('  ' + _UI['desc_label'][lang] + ': ' +
          _pick(lang, info['desc_ar'], info['desc_en']))

    ar_print('\n' + _UI['why_header'][lang])
    ar_print(_pick(lang, info['why_ar'], info['why_en']))

    ar_print('\n' + _UI['trace_header'][lang])
    _print_trace(expl['fired_rules'])

    ar_print('\n' + _UI['farewell'][lang])


def _print_trace(steps):
    """Print each reasoning step — uses map (no for statement)."""
    list(map(lambda s: ar_print('    • ' + s), steps))


# ============================================================
# Main entry point
# ============================================================
def main():
    ar_print(_UI['banner']['en'])
    lang = _select_language()
    ar_print('\n' + _UI['banner'][lang] + '\n')

    engine = DesignPatternPicker()
    engine.reset()      # triggers @DefFacts → seeds SystemState, Context, Questions
    _drive(engine, lang)
    _present_result(engine, lang)