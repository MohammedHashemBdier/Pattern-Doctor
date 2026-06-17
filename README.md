# PATTERN DOCTOR - DESIGN PATTERN PICKER— Expert System

> **Knowledge Base Systems Course** · Damascus University
> Faculty of Information Engineering · **Prof. George Anwar Karaz**
> University Graduation-level Mini-Project

نظام خبير قائم على القواعد يوجّه المبرمج عبر 3–5 أسئلة ليقترح أحد 10 أنماط تصميم شهيرة، مع ميزة **«لماذا؟» (Meta-Reasoning)** التي تشرح سبب التوصية.

A Rule-Based Expert System that guides a programmer through 3–5 questions
and recommends one of 10 famous design patterns, with a **"Why?"**
meta-reasoning feature explaining each recommendation.

---

## 1. الفكرة | The Idea

يطرح النظام أسئلة تدريجية عن طبيعة المشكلة (إنشاء كائنات، هيكلة، سلوك) ثم
يطابق الإجابات مع قاعدة معرفية من **48 قاعدة إنتاجية** ليقترح النمط الأنسب
مع تبرير منطقي كامل.

The system asks progressive questions about the problem's nature (creation,
structure, behavior) then matches answers against a knowledge base of
**48 production rules** to recommend the best pattern with full reasoning.

---

## 2. التقنيات | Technology

| المكوّن        | الأداة                                              |
| -------------- | --------------------------------------------------- |
| لغة البرمجة    | Python 3.12                                         |
| محرك الاستدلال | **experta 1.9.4** (Rete Algorithm — fork of pyknow) |
| الواجهة        | CLI ثنائية اللغة (عربي / إنكليزي)                   |
| قاعدة البيانات | ذاكرة عاملة (Working Memory) — حقائق فقط            |

---

## 3. التشغيل | How to Run

```bash
cd design-pattern-picker
pip install -r requirements.txt
python3 run.py
```

ثم اختر اللغة (1 = English, 2 = العربية) وأجب عن الأسئلة بـ `yes`/`no`
(أو `نعم`/`لا`).

---

## 4. بنية المشروع | Project Structure

```
design-pattern-picker/
├── requirements.txt      ← experta dependency
├── run.py                ← Entry point (thin launcher, zero logic)
├── facts.py              ← Step 1: Fact class definitions (Working Memory schema)
├── questions.py          ← Bilingual question catalog (12 questions, data only)
├── patterns.py           ← 10 patterns metadata + bilingual justifications
├── knowledge_base.py     ← Step 2+3: 48 @Rule definitions (Inference Engine)
├── cli.py                ← Step 4: CLI driver (Interface Layer)
└── README.md             ← This file
```

### الفصل المعماري | Architectural Separation

```
┌─────────────────────────────────────────────┐
│  INTERFACE LAYER   (cli.py)                 │  ← I/O only, no decisions
├─────────────────────────────────────────────┤
│  INFERENCE ENGINE  (knowledge_base.py)      │  ← ALL decisions via @Rule
├─────────────────────────────────────────────┤
│  WORKING MEMORY    (facts.py)               │  ← state as facts
└─────────────────────────────────────────────┘
```

---

## 5. القيود الأكاديمية والامتثال | Academic Constraints & Compliance

### القيود (Zero Tolerance)

| #   | القيد                                                                | الامتثال                                          |
| --- | -------------------------------------------------------------------- | ------------------------------------------------- |
| 1   | منع `if`/`elif`/`else`/`for`/`while` في منطق القواعد ومحرك الاستدلال | ✅ صفر في `knowledge_base.py`                     |
| 2   | منع إخفاء المنطق الشرطي في helper functions / lambdas                | ✅ الدوال المساعدة نقية فقط (بناء حقائق، استعلام) |
| 3   | تفكير Rule-Based بحت عبر Rete                                        | ✅ كل المطابقة عبر `@Rule` + `NOT` + `AS`         |
| 4   | أفعال صالحة فقط: `declare`/`modify`/`retract`                        | ✅ جسم كل قاعدة يحتوي حصراً عليها                 |
| 5   | إدارة الحوار عبر Control Facts                                       | ✅ `SystemState(current_stage=...)` تقود الحوار   |

### إثبات الامتثال | Compliance Proof

```bash
# تدقيق صريح: صفر عبارات if/elif/else/for/while على مستوى العبارات
grep -nE '^\s*(if|elif|else|for|while)\b' *.py
# → No matches found
```

**كيف يُدار الحوار دون `while`؟**
عبر Control Facts: حقيقة `SystemState(current_stage='ask_X')` تُفعّل قاعدة
`r_ask_qX` التي تُصرِّح `PendingQuestion(qid='QX')`. طبقة الواجهة تقرأ
السؤال، تجمع الجواب، تُصرِّح `UserAnswer`. ثم قاعدة `r_qX_yes/no` تُعدّل
`Context` وتنقل `current_stage` للمرحلة التالية. لا حلقة تكرارية إطلاقاً.

**كيف تتجنب طبقة الواجهة `if`/`while`؟**

- **الـ recursion** بدل `while` (الدالة `_drive` تستدعي نفسها)
- **boolean short-circuit** بدل `if/else`: `_has_fact(...) or _advance(...)`
- **dict lookups** بدل سلاسل `if`: `_ANSWER_MAP.get(raw) or _reask(...)`
- **`any`/`next`/`filter`/`map`** بدل الحلقات

---

## 6. الأنماط العشرة | The 10 Design Patterns

| النمط            | التصنيف    | شرط التوصية                              |
| ---------------- | ---------- | ---------------------------------------- |
| Singleton        | Creational | `needs_single_instance=True` + ليس عائلة |
| Factory Method   | Creational | `needs_deferred_creation=True`           |
| Abstract Factory | Creational | `needs_family_of_objects=True`           |
| Adapter          | Structural | `needs_interface_compat=True`            |
| Decorator        | Structural | `needs_dynamic_decoration=True`          |
| Facade           | Structural | `needs_subsystem_simplification=True`    |
| Command          | Behavioral | `needs_request_encapsulation=True`       |
| State            | Behavioral | `needs_state_based_behavior=True`        |
| Strategy         | Behavioral | `needs_algorithm_variants=True`          |
| Observer         | Behavioral | `needs_change_notification=True`         |

---

## 7. جرد القواعد | Rule Inventory (48 rules)

| القسم                    | العدد  | الوظيفة                                               |
| ------------------------ | ------ | ----------------------------------------------------- |
| A — Ask rules            | 12     | تُصرِّح `PendingQuestion` عند الدخول لكل مرحلة        |
| B — Answer rules         | 24     | تعالج yes/no، تُحدّث `Context`، تنقل المرحلة          |
| C — Recommendation rules | 10     | تُفعّل عند `stage='ready'`، تُصرِّح التوصية + التفسير |
| D — Fallback rule        | 1      | لا يوجد نمط مطابق (salience -1)                       |
| E — Finalize rule        | 1      | تُصرِّح `DialogComplete` (salience -10)               |
| **المجموع**              | **48** |                                                       |

---

## 8. ميزة «لماذا؟» | The "Why?" Feature (Meta-Reasoning)

عندما تُفعّل قاعدة توصية، تُصرِّح **حقيقتين** معاً:

1. `RecommendedPattern(pattern_name, category)` — التوصية
2. `Explanation(pattern_name, justification_ar, justification_en, fired_rules)` — التفسير

حقل `fired_rules` يخزّن **أثر الاستدلال** (reasoning trace) كسلسلة خطوات منطقية،
مما يتيح للمستخدم رؤية التبرير الكامل. هذا يحقق متطلب **المحاضرة 4**
(Meta-Reasoning).

**مثال على الأثر:**

```
Reasoning Trace:
    • Q1 = yes  →  category = creational
    • Q3 = yes  →  needs_single_instance = True
    • Q5 = no   →  needs_family_of_objects = False
    • RULE r_rec_singleton FIRED  →  Singleton
```

---

## 9. دورة حياة النظام الخبير | Expert System Life Cycle (Lecture 5)

| المرحلة          | التطبيق في المشروع                                     |
| ---------------- | ------------------------------------------------------ |
| 1. تحديد المشكلة | اختيار 10 أنماط تصميم شهيرة                            |
| 2. جمع المعرفة   | استخراج القواعد من مراجع GoF                           |
| 3. التمثيل       | قواعد `IF context/symptoms THEN pattern + explanation` |
| 4. التنفيذ       | محرك استدلال بـ experta (Rete)                         |
| 5. التفسير       | ميزة «لماذا؟» عبر حقائق `Explanation`                  |

---

## 10. سيناريوهات الاختبار | Test Scenarios

كل سيناريو يُختبر بتغذية الإجابات عبر stdin:

| السيناريو             | الإجابات                     | النتيجة المتوقعة       |
| --------------------- | ---------------------------- | ---------------------- |
| Singleton             | yes → yes → no               | ✅ Singleton           |
| Factory Method        | yes → no → yes               | ✅ Factory Method      |
| Abstract Factory (a)  | yes → yes → yes              | ✅ Abstract Factory    |
| Abstract Factory (b)  | yes → no → no → yes          | ✅ Abstract Factory    |
| Adapter               | no → yes → yes               | ✅ Adapter             |
| Decorator             | no → yes → no → yes          | ✅ Decorator           |
| Facade                | no → yes → no → no → yes     | ✅ Facade              |
| Command               | no → no → yes                | ✅ Command             |
| State                 | no → no → no → yes           | ✅ State               |
| Strategy              | no → no → no → no → yes      | ✅ Strategy            |
| Observer              | no → no → no → no → no → yes | ✅ Observer            |
| Fallback (creational) | yes → no → no → no           | ✅ No Suitable Pattern |
| Fallback (behavioral) | no → no → no → no → no → no  | ✅ No Suitable Pattern |

كل السيناريوهات الـ 13 مُختبرة ونجحت ✅

---

## 11. الفريق | Team

مشروع مادة «أنظمة قواعد المعرفة» — كلية هندسة المعلوماتية، جامعة دمشق.
إشراف: **الأستاذ الدكتور جورج أنور كراز**.

---

_نظام خبير قائم على القواعد (Rule-Based Expert System) باستخدام خوارزمية Rete
عبر مكتبة experta — التزام كامل بالقيود الأكاديمية الصارمة._
