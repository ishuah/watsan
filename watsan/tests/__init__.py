#from [Project Name].[App Name].tests.[filename] import *  
from Tests import *
from MapTests import *

#starts the test suite  
__test__= {  
    'basicTests': [Tests],
    'mapTests': [MapTests],
}