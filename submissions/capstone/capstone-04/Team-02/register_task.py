import subprocess

task_name = "SleepsiaDaily8AMReport"
# Use short 8.3 path or escaped quotes
py_exe = "python.exe"
script_path = r'C:\Users\Taniya Gupta\Desktop\report\send_8am_report.py'

cmd = f'schtasks /Create /F /TN "{task_name}" /TR "{py_exe} \"{script_path}\"" /SC DAILY /ST 08:00'
print("Command:", cmd)

res = subprocess.run(['schtasks', '/Create', '/F', '/TN', task_name, '/TR', f'python.exe "{script_path}"', '/SC', 'DAILY', '/ST', '08:00'], capture_output=True, text=True)
print("STDOUT:", res.stdout)
print("STDERR:", res.stderr)
if res.returncode == 0:
    print("SUCCESS: 8:00 AM Daily Task successfully registered!")
