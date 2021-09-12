class BaseMarketObjectManager:
    """
    this class provides the basic functionality will repetitively be using in Market subclasses
    all other objects will inherit the basic functionality
    """
    targetObject = None

    def __init__(self, request=None):
        self.querySet = dict()
        self.order_by = False
        self.limits = None
        self.price = False
        self.request = request

    @classmethod
    def selectById(cls, identifier):
        return cls.targetObject.objects.get(id=identifier)

    def orderBy(self, order_by_string):
        self.order_by = order_by_string
        return self

    def limitsBy(self, lower_boundary_band, higher_boundary_band):
        self.limits = [lower_boundary_band, higher_boundary_band]
        return self

    @classmethod
    def getClass(cls):
        return cls

    def fetch(self):
        objects = self.getClass().targetObject.objects.filter(**self.querySet).order_by(
            self.order_by) if self.order_by else self.getClass().targetObject.objects.filter(**self.querySet)
        return objects[self.limits[0]:self.limits[1]] if self.limits else objects
