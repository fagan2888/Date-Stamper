from distutils.core import setup
import py2exe
import os
import shutil

data = [('',['build/msvcp90.dll',]),
		('',['help.inc',])]

for files in os.listdir('icons'):
	f1 = os.path.join('icons',files)
	if os.path.isfile(f1) and f1.split('.')[-1] != 'psd':
		f2 = 'icons',[f1]
		data.append(f2)

shutil.copy('build/msvcp90.dll','msvcp90.dll')

NAME = 'Date Stamper'
VER	= '2.0'
ID = '{{6638951C-0E99-4FAF-AAF1-B283912E7DFF}'
URL='http://www.suever.net/software'

OUTDIR = os.path.join('dist',''.join([NAME,' ',VER]))
EXE = 'DateStamper.exe'

setup(
	name = NAME,
	version = VER,
	description = 'A Date imprinting Utility',
	author = 'Jonathan Suever',
    options = {'py2exe': {'bundle_files': 1,
						  'dist_dir':OUTDIR}},
	data_files = data,
    windows = [{"script":'DateStamper.pyw',
				"icon_resources":[(1,"icons/icon.ico")]}],
    zipfile = None,
)
try:
	shutil.rmtree(os.path.join(OUTDIR,'tcl'))
except:
	print('unable to find tcl. skipping')

os.remove(os.path.join(OUTDIR,'w9xpopen.exe'))
shutil.rmtree(os.path.join('build','bdist.win32'))
#shutil.rmtree(os.path.join('build','lib'))
os.remove('msvcp90.dll')

INSTALLER = '%s_%s.setup' % (EXE.replace('.exe',''),VER.replace('.','_'))
INSTALLER = INSTALLER.replace(' ','_')

# Construct the configuration string for Inno Setup
innoDict = {'AppId':ID,
            'AppName':NAME,
            'AppVerName':'%s %s' % (NAME,VER),
            'AppPublisher':'Jonathan Suever',
            'AppPublisherURL':URL,
            'AppSupportURL':URL,
            'AppUpdatesURL':URL,
            'DefaultDirName':'{pf}\%s' % NAME,
            'DefaultGroupName':NAME,
            'OutputDir':'dist',
            'OutputBaseFilename':INSTALLER,
            'Compression':'lzma',
            'SolidCompression':'yes'}

innoinput = '[Setup]\n'

for key,value in innoDict.items():
    innoinput = ''.join([innoinput,'%s=%s\n' % (key,value)])

lang = '[Languages]\nName: "english"; MessagesFile: "compiler:Default.isl"\n'
task = '[Tasks]\nName:"desktopicon"; Description: "{cm:CreateDesktopIcon}";GroupDescription:"{cm:AdditionalIcons}";\n'

OUTEXE = os.path.join(OUTDIR,EXE)
INCLUDES = os.path.join(OUTDIR,'*')

files = '''[Files]
Source: "%s"; DestDir: "{app}"; Flags: ignoreversion
Source: "%s"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs'''

files = files % (OUTEXE,INCLUDES)

ICONFILE = 'icons/icon.ico'

icons = '''[Icons]
Name: "{group}\%s"; Filename: "{app}\%s"; IconFilename: {app}\%s; IconIndex: 0; WorkingDir: "{app}"
Name: "{userdesktop}\%s"; Filename: "{app}\%s"; Tasks: desktopicon; IconFilename: {app}\%s; IconIndex: 0'''

icons = icons % (NAME,EXE,ICONFILE,NAME,EXE,ICONFILE)

run = '''[Run]
Filename: "{app}\%s"; Description: "{cm:LaunchProgram,%s}"; Flags: nowait postinstall skipifsilent'''

run = run % (EXE,NAME)

fullfile = '\n'.join([innoinput,lang,task,files,icons,run])

# Write configuration to a temporary file
f = open('wizard.iss','w')
f.write(fullfile)
f.close()

print('Now Compiling using Inno Setup 5.')
print('Be sure that it is installed, and added to your system PATH')
os.system('Compil32 /cc wizard.iss')
os.remove('wizard.iss')
print('Successfully created application and installer!')
