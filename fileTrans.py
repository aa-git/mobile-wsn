
def path_to_file(file_name,path):
    file_ = open(file_name,"w")
    file_.write(str(len(path))+"\n")
    
    for i in range(len(path)):
        file_.write(str(path[i])+" ")
        
    file_.close()

def coordintes_to_file(file_name ,graph):
    file_ = open(file_name,"w")
    file_.write(str(len(graph))+"\n")
    
    for i in range(len(graph)):
        file_.write(str(graph[i][0])+" "+str(graph[i][1])+"\n")
        
    file_.close()

def is_not_true(file_name):
    try:
        file_ = open(file_name,"r")
        content = file_.read()
        if content=="TRUE":
            return 0
        return 1
    except:
        return 1

def reinforce_path_to_console(file_name):
    try:
        file_ = open(file_name,"r")
        path = file_.read().split(" ")[:-1]
        print ("\n\nReinforced path ", path , "\n\n")
        path = list(map(int,path))
        file_.close()
        return (1,path)
    except:
        return (0,0)
    
def ACO_path_to_console(file_name):
    try:
        file_ = open(file_name,"r")
        path = file_.read()
        print ("\n\nACO path ", path , "\n\n")
        file_.close()
        return 1
    except:
        return 0
