; Instalador de Miausic (NSIS). Se compila con herramientas/construir.py
Unicode true
!include "MUI2.nsh"
!include "FileFunc.nsh"
!include "Sections.nsh"

!ifndef VERSION
  !define VERSION "1.0.0"
!endif
!define UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\Miausic"
!define PYW "$INSTDIR\.venv\Scripts\pythonw.exe"
!define MAIN "$INSTDIR\app\main.py"

Name "Miausic"
OutFile "${SALIDA}"
InstallDir "$LOCALAPPDATA\Programs\Miausic"
InstallDirRegKey HKCU "Software\Miausic" "Carpeta"
RequestExecutionLevel user
SetCompressor /SOLID lzma
BrandingText "Miausic ${VERSION}"
VIProductVersion "${VERSION}.0"
VIAddVersionKey "ProductName" "Miausic"
VIAddVersionKey "FileDescription" "Instalador de Miausic"
VIAddVersionKey "FileVersion" "${VERSION}"
VIAddVersionKey "ProductVersion" "${VERSION}"
VIAddVersionKey "CompanyName" "Miausic"
VIAddVersionKey "LegalCopyright" "Miausic"

!define MUI_ICON "${RECURSOS}\miausic.ico"
!define MUI_UNICON "${RECURSOS}\miausic.ico"
!define MUI_WELCOMEFINISHPAGE_BITMAP "${RECURSOS}\instalador_lateral.bmp"
!define MUI_UNWELCOMEFINISHPAGE_BITMAP "${RECURSOS}\instalador_lateral.bmp"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_RIGHT
!define MUI_HEADERIMAGE_BITMAP "${RECURSOS}\instalador_cabecera.bmp"
!define MUI_ABORTWARNING
!define MUI_ABORTWARNING_TEXT "¿Seguro que quieres cancelar la instalación de Miausic?"

!define MUI_WELCOMEPAGE_TITLE "Bienvenido a Miausic"
!define MUI_WELCOMEPAGE_TEXT "Miausic es tu reproductor de música con Michi.$\r$\n$\r$\nPegas links de YouTube, SoundCloud y más, los guardas en playlists, y Michi aprende tus gustos para recomendarte música nueva. Sin abrir Chrome y gastando muy poco.$\r$\n$\r$\nEl instalador prepara todo solo (unos minutos, necesita internet)."
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_TITLE "¡Miausic está instalada!"
!define MUI_FINISHPAGE_TEXT "Pega tu primer link y que empiece la música. Para las recomendaciones, entra en Ajustes y pega tu clave gratis de Last.fm."
!define MUI_FINISHPAGE_RUN
!define MUI_FINISHPAGE_RUN_TEXT "Abrir Miausic"
!define MUI_FINISHPAGE_RUN_FUNCTION AbrirMiausic
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_LANGUAGE "Spanish"

!macro CerrarMiausic
  DetailPrint "Cerrando Miausic si está abierta..."
  nsExec::ExecToLog `powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-CimInstance Win32_Process | Where-Object { $$_.ExecutablePath -like '$INSTDIR\*' } | ForEach-Object { Stop-Process -Id $$_.ProcessId -Force -ErrorAction SilentlyContinue }"`
  Pop $0
  Sleep 800
!macroend

Section "Miausic (necesario)" SecApp
  SectionIn RO
  SetDetailsPrint both
  !insertmacro CerrarMiausic
  SetOutPath "$INSTDIR"
  File /r "${APPDIR}\*.*"

  DetailPrint "Preparando Python, las librerías y el motor de audio (puede tardar unos minutos)..."
  nsExec::ExecToLog `powershell -NoProfile -ExecutionPolicy Bypass -File "$INSTDIR\instalacion\preparar.ps1" -Carpeta "$INSTDIR"`
  Pop $0
  StrCmp $0 "0" preparado
    MessageBox MB_ICONSTOP "No se pudo preparar Miausic (código $0).$\r$\nRevisa tu conexión a internet y vuelve a ejecutar el instalador." /SD IDOK
    Abort
  preparado:

  CreateShortcut "$SMPROGRAMS\Miausic.lnk" "${PYW}" '"${MAIN}"' "$INSTDIR\recursos\miausic.ico" 0 SW_SHOWNORMAL "" "Tu música con Michi"

  WriteUninstaller "$INSTDIR\Desinstalar Miausic.exe"
  WriteRegStr HKCU "Software\Miausic" "Carpeta" "$INSTDIR"
  WriteRegStr HKCU "${UNINST_KEY}" "DisplayName" "Miausic"
  WriteRegStr HKCU "${UNINST_KEY}" "DisplayVersion" "${VERSION}"
  WriteRegStr HKCU "${UNINST_KEY}" "DisplayIcon" "$INSTDIR\recursos\miausic.ico"
  WriteRegStr HKCU "${UNINST_KEY}" "Publisher" "Miausic"
  WriteRegStr HKCU "${UNINST_KEY}" "InstallLocation" "$INSTDIR"
  WriteRegStr HKCU "${UNINST_KEY}" "UninstallString" '"$INSTDIR\Desinstalar Miausic.exe"'
  WriteRegStr HKCU "${UNINST_KEY}" "QuietUninstallString" '"$INSTDIR\Desinstalar Miausic.exe" /S'
  WriteRegDWORD HKCU "${UNINST_KEY}" "NoModify" 1
  WriteRegDWORD HKCU "${UNINST_KEY}" "NoRepair" 1
  ${GetSize} "$INSTDIR" "/S=0K" $1 $2 $3
  WriteRegDWORD HKCU "${UNINST_KEY}" "EstimatedSize" $1
SectionEnd

Section "Acceso directo en el escritorio" SecEscritorio
  CreateShortcut "$DESKTOP\Miausic.lnk" "${PYW}" '"${MAIN}"' "$INSTDIR\recursos\miausic.ico" 0 SW_SHOWNORMAL "" "Tu música con Michi"
  WriteRegDWORD HKCU "Software\Miausic" "Escritorio" 1
SectionEnd

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecApp} "El programa, su Python propio, las librerías y el motor de audio. Tu biblioteca se guarda aparte y nunca se borra al actualizar."
  !insertmacro MUI_DESCRIPTION_TEXT ${SecEscritorio} "Un ícono de Michi con audífonos en el escritorio."
!insertmacro MUI_FUNCTION_DESCRIPTION_END

Function .onInit
  ; en una actualización silenciosa se respetan las opciones de la primera instalación
  IfSilent 0 fin
    ReadRegDWORD $0 HKCU "Software\Miausic" "Escritorio"
    StrCmp $0 "1" +2
      !insertmacro UnselectSection ${SecEscritorio}
  fin:
FunctionEnd

Function .onInstSuccess
  ; tras una actualización silenciosa, Miausic se vuelve a abrir
  IfSilent 0 +2
    Exec '"${PYW}" "${MAIN}"'
FunctionEnd

Function AbrirMiausic
  Exec '"${PYW}" "${MAIN}"'
FunctionEnd

Section "Uninstall"
  !insertmacro CerrarMiausic
  Delete "$SMPROGRAMS\Miausic.lnk"
  Delete "$DESKTOP\Miausic.lnk"
  RMDir /r "$INSTDIR"
  DeleteRegKey HKCU "${UNINST_KEY}"
  DeleteRegKey HKCU "Software\Miausic"
  MessageBox MB_YESNO|MB_ICONQUESTION "¿Borrar también tu biblioteca, playlists y gustos?$\r$\n(Si dices que no, siguen ahí si vuelves a instalar Miausic.)" /SD IDNO IDNO conservar
    RMDir /r "$APPDATA\Miausic"
    RMDir /r "$LOCALAPPDATA\Miausic"
  conservar:
SectionEnd
