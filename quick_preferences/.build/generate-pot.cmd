@pushd
@cd ..
python C:\Python310\Tools\i18n\pygettext.py -d quick-preferences -p translations^
 action.py config.py ..\common\common_*.py
@popd
