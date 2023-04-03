class Shot:
    def __init__(self, **kwargs):
        # def __init__(self,ringe,teiler,x,y):
        self.ringe = kwargs.get("ringe", None)
        self.teiler = kwargs.get("teiler", 9999999)
        self.x = kwargs.get("x", None)
        self.y = kwargs.get("y", None)
        # self.k_distance = None
        # self.k_nearest = []
        # self.lrd = None
        # self.lof = None
        # self.ringe=ringe
        # self.teiler=teiler
        # self.x=x
        # self.y=y

    def __str__(self):
        return f"{self.ringe}"

    def __repr__(self):
        return f"{self.ringe}"

    def __lt__(self, other):
        return self.teiler > other.teiler
