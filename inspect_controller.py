import importlib, os, sys
os.chdir(r'c:/Users/Kenwo/OneDrive/Documents/cd password-manager')
sys.modules.pop('src.adapters.controllers.credential_resource', None)
mod = importlib.import_module('src.adapters.controllers.credential_resource')
print('has LoginResource', hasattr(mod, 'LoginResource'))
print('has RegisterUserResource', hasattr(mod, 'RegisterUserResource'))
print(mod.__file__)
print(open(mod.__file__, encoding='utf-8').read())
