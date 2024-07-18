from guiManager import *

app = MorseMaster()
app.iconbitmap('iconAssets/morseMasterIcon.ico')
app.title('MorseMaster')
app.minsize(750,350)

textTranslatorWidgetObjects = app.tabBar.textTranslatorTab.winfo_children()
textTranslatorObject = {}
for widgetObject in textTranslatorWidgetObjects:
    if hasattr(widgetObject, 'Name'):
        textTranslatorObject[widgetObject.Name] = widgetObject

app.mainloop()