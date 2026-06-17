"""
PATTERN DOCTOR - DESIGN PATTERN PICKER —  Bilingual Question Catalog
=====================================================================
Knowledge Base Systems Course  —  Damascus University

This module holds the static catalog of questions (data only, no logic).
Each ``Question`` fact is bilingual (Arabic + English) to satisfy the
project's dual-language requirement.

Catalog layout (12 questions, 12 question-stages):
  Q1  category discriminator  → creational?
  Q2  category discriminator  → structural? (else behavioral)
  Q3  creational signal       → single instance?      (Singleton)
  Q4  creational signal       → deferred creation?    (Factory Method)
  Q5  creational signal       → family of objects?    (Abstract Factory)
  Q6  structural signal       → interface compat?     (Adapter)
  Q7  structural signal       → dynamic decoration?   (Decorator)
  Q8  structural signal       → subsystem simplify?   (Facade)
  Q9  behavioral signal       → request encapsulation?(Command)
  Q10 behavioral signal       → state-based behavior? (State)
  Q11 behavioral signal       → algorithm variants?   (Strategy)
  Q12 behavioral signal       → change notification?  (Observer)

A single session asks only 3-5 of these (branching decision tree),
well within the "5-10 questions" requirement.
=====================================================================
"""

from facts import Question

QUESTIONS = [
    Question(
        qid='Q1',
        text_ar='هل مشكلتك تتعلق بإنشاء الكائنات (Object Creation)؟',
        text_en='Is your problem related to object CREATION?',
    ),
    Question(
        qid='Q2',
        text_ar='هل مشكلتك تتعلق بتركيب وهيكلة الكائنات (Object Structure)؟',
        text_en='Is your problem related to object STRUCTURE / composition?',
    ),
    Question(
        qid='Q3',
        text_ar='هل تحتاج إلى وجود نسخة واحدة فقط من الكائن عبر النظام كله؟',
        text_en='Do you need a SINGLE instance of an object across the entire system?',
    ),
    Question(
        qid='Q4',
        text_ar='هل تحتاج لتأجيل تحديد نوع الكائن المُنشأ إلى وقت التشغيل (Runtime)؟',
        text_en='Do you need to DEFER the decision of which object to create until runtime?',
    ),
    Question(
        qid='Q5',
        text_ar='هل تحتاج لإنشاء عائلة من الكائنات المترابطة معاً؟',
        text_en='Do you need to create a FAMILY of related objects together?',
    ),
    Question(
        qid='Q6',
        text_ar='هل تحتاج لجعل واجهة غير متوافقة تعمل مع واجهة أخرى متوقعة؟',
        text_en='Do you need to make an INCOMPATIBLE interface work with an expected one?',
    ),
    Question(
        qid='Q7',
        text_ar='هل تحتاج لإضافة سلوك لكائن بشكل ديناميكي دون تعديل أصله؟',
        text_en='Do you need to ADD behavior to an object DYNAMICALLY without modifying its class?',
    ),
    Question(
        qid='Q8',
        text_ar='هل تريد تبسيط واجهة نظام فرعي معقد لتقديم واجهة موحدة؟',
        text_en='Do you want to SIMPLIFY a complex subsystem by providing a unified interface?',
    ),
    Question(
        qid='Q9',
        text_ar='هل تحتاج لتغليف الطلب (Request) ككائن مستقل قابل للتخزين والتأجيل؟',
        text_en='Do you need to ENCAPSULATE a request as an independent object (storable / deferrable)?',
    ),
    Question(
        qid='Q10',
        text_ar='هل يتغير سلوك الكائن تبعاً لحالته الداخلية (State)؟',
        text_en="Does the object's behavior CHANGE depending on its internal state?",
    ),
    Question(
        qid='Q11',
        text_ar='هل لديك خوارزميات متعددة قابلة للتبديل وقت التشغيل؟',
        text_en='Do you have multiple ALGORITHMS that can be swapped at runtime?',
    ),
    Question(
        qid='Q12',
        text_ar='هل تحتاج لإشعار كائنات متعددة تلقائياً عند تغير حالة كائن ما؟',
        text_en='Do you need to automatically NOTIFY multiple objects when another object changes?',
    ),
]
