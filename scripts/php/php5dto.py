import stringtemplate3,os,sys
from asdox import asBuilder,asModel

if len(sys.argv) > 3:
    src = sys.argv[1]
    dest = sys.argv[2]
    tmpl = sys.argv[3]
    
    if not os.path.isdir(src):
        sys.exit("Invalid source path: " + src)
    if not os.path.isdir(dest):
        sys.exit("Invalid destination path: " + dest)
    if not os.path.isfile(tmpl):
        sys.exit("Invalid template file: " + tmpl)
else:
    sys.exit("Script required three arguments: <source> <destination> <template>")

builder = asBuilder.Builder()
builder.addSource(src)

initMap = {'Boolean':'false','int':'0','Number':'0','String':'""','unit':'0','Date':'NULL'}
for pkg in builder.packages.values():
    for cls in pkg.classes.values():
        head,tail = os.path.split(tmpl)
        group = stringtemplate3.StringTemplateGroup(tail,head)
        template = group.getInstanceOf("php5dto")
        tmp = asModel.ASClass()
        tmp.objects = dict()
        tmp.collections = dict()
        tmp.properties = dict()
        tmp.name = cls.name

        for var in cls.variables.values():
            if var.visibility == "public":
                var.capitalize = var.name.capitalize()
                if var.type in initMap:
                    var.init = initMap[var.type]
                    if var.isProperty:
                        tmp.properties[var.name] = var
                    else:
                        tmp.variables[var.name] = var
                else:
                    for meta in var.metadata:
                        if meta.name == "ValueObject":
                            var.init = "new " + var.type + "()"
                            tmp.objects[var.name] = var
                        if meta.name == "ValueObjectCollection":
                            var.type = meta.params["type"]
                            var.init = "array()"
                            tmp.collections[var.name] = var
    
        template["class"] = tmp
        file = open( dest + "\\" + tmp.name + '.php','w')
        file.write( str(template) )
        file.close()
