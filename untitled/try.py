import datetime

projectId = 1

now_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
name = "到机房降低.rvt"
name = name.split(".")
name_1 = str(projectId)+ str(now_time)
name = name_1+'.'+name[1]

print(name)