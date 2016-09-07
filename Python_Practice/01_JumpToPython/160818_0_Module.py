#일종의 Lib 추가와 같이 Python의 기능을 묶은 단위의 Module을 Import(C의 include)하여 사용
#1) PyCharm기준 File/Settings(Alt + F7)/Project/ProjectInterpeter/Option Button/More/
#   Show path for the selected interpreter/Path Add
#
#2) sys.path.append(경로)
#
#3) PYTHONEPATH 환경변수 내 경로 입력

import  MathHelper                   #import ModuleName                 : Module을 포함하고 내부 기능 사용
from MathHelper import safe_mul     #from ModuleName import ModuleFunc : Module내 지정 기능을 ModuleName.Function 대신 바로 Fuction을 쓰기 위해 포함시킨다
#from MathHelper import *            #Module 내 모든 기능을 from ~ import 와 같이 사용하게 된다


print(MathHelper.sum(1, 2, 3, 4))
print(safe_mul(5, 3))

cm = MathHelper.CircleMath()
print(cm.PI)
