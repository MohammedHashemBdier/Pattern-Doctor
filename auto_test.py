import subprocess
import sys
import os
import arabic_reshaper
from bidi.algorithm import get_display

"""
Automated Test Script for Design Pattern Picker (Venv-Aware)
============================================================
"""

def ar_print(text):
    reshaped = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped)
    print(bidi_text)

def get_python_executable():
    """
    يحاول العثور على بايثون الموجود داخل الـ venv
    """
    # نحصل على المسار الكامل للمجلد الحالي
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # نفترض أن الـ venv في مجلد اسمه 'venv' بجانب المشروع
    # في الويندوز الملف التنفيذي داخل venv/Scripts/python.exe
    venv_python = os.path.join(current_dir, "venv", "Scripts", "python.exe")
    
    if os.path.exists(venv_python):
        ar_print(f"[INFO] Using Venv Python: {venv_python}")
        return venv_python
    else:
        ar_print(f"[WARNING] Could not find venv at: {venv_python}")
        ar_print(f"[WARNING] Falling back to System Python: {sys.executable}")
        ar_print("[WARNING] This might cause the 'frozendict' error if not fixed globally.")
        return sys.executable

def run_scenario(name, inputs):
    separator = f"{'#'*60}"
    ar_print(f"\n{separator}")
    ar_print(f"# SCENARIO: Testing '{name}'")
    ar_print(f"{'#'*60}\n")

    script_path = "run.py"
    if not os.path.exists(script_path):
        ar_print(f"Error: Could not find {script_path}.")
        return False

    # تحديد نسخة بايثون الصحيحة
    python_exe = get_python_executable()

    # إعداد الترميز (Encoding Fix)
    my_env = os.environ.copy()
    my_env["PYTHONIOENCODING"] = "utf-8"

    try:
        process = subprocess.Popen(
            [python_exe, script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',
            errors='replace',
            env=my_env
        )
        
        input_data = "\n".join(inputs) + "\n"
        stdout, stderr = process.communicate(input=input_data, timeout=10)
        
        ar_print(stdout)
        
        if stderr:
            # نطبع الأخطاء فقط إذا وجدنا نصاً حقيقياً فيها (تجاهل تحذيرات بايثون المزعجة أحياناً)
            stderr_clean = stderr.strip()
            if stderr_clean and "DeprecationWarning" not in stderr_clean:
                ar_print("!!! ERRORS/WARNINGS !!!")
                ar_print(stderr)
            
        return process.returncode == 0
        
    except subprocess.TimeoutExpired:
        process.kill()
        ar_print("Error: Program timed out.")
        return False
    except Exception as e:
        ar_print(f"Unexpected Error: {e}")
        return False

# تعريف الحالات
scenarios = {
    "1. Singleton":             ["1", "y", "y", "n"],
    "2. Factory Method":        ["1", "y", "n", "y"],
    "3. Abstract Factory":      ["1", "y", "n", "n", "y"],
    
    "4. Adapter":               ["1", "n", "y", "y"],
    "5. Decorator":             ["1", "n", "y", "n", "y"],
    "6. Facade":                ["1", "n", "y", "n", "n", "y"],
    
    "7. Command":               ["1", "n", "n", "y"],
    "8. State":                 ["1", "n", "n", "n", "y"],
    "9. Strategy":              ["1", "n", "n", "n", "n", "y"],
    "10. Observer":             ["1", "n", "n", "n", "n", "n", "y"],
    
    "11. Fallback (No Pattern)": ["1", "y", "n", "n", "n"],
}

# التنفيذ
ar_print("Starting Automated Testing (Venv-Aware + UTF-8 Fixed)...")

results = {}
for name, inputs in scenarios.items():
    success = run_scenario(name, inputs)
    results[name] = success

# التقرير النهائي
ar_print(f"\n{'='*60}")
ar_print("FINAL TEST REPORT")
ar_print(f"{'='*60}")

all_passed = True
for name, success in results.items():
    status = "✅ PASS" if success else "❌ FAIL"
    ar_print(f"{name:<30} {status}")
    if not success:
        all_passed = False

ar_print(f"{'='*60}")
if all_passed:
    ar_print("RESULT: ALL TESTS PASSED!")
else:
    ar_print("RESULT: SOME TESTS FAILED.")