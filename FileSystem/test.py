from ProjectSaver import ProjectSaver

list = ["AddEntity(name='Entity0', model='cube', color='#5d534aff', )",
        "AddEntity(name='Entity1', model='cube', color='#5d538aff', )"]

ProjectSaver("My First Project", None, None, None, None, None, None,
             Items=list,
             Path="../Saves/",
             SaveOnlyIfProjectAlreayExists=False)
