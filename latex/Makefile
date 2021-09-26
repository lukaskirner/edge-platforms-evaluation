rwildcard=$(foreach d,$(wildcard $(1:=/*)),$(call rwildcard,$d,$2) $(filter $(subst *,%,$2),$d))

glos:
	makeglossaries -d .tmp main

inkscape:
	for i in $(call rwildcard,assets,*.svg);do inkscape -D -z --file=$$i --export-pdf=$${i%.svg}.pdf --export-latex;done
