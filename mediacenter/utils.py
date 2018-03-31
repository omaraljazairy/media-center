from enum import Enum
import logging

logger = logging.getLogger('utils')

class Choices(Enum):
    @classmethod
    def choices(cls):
        return tuple((choice.name, choice.value) for choice in cls)


class QuerySetConverter:

    def to_list(self, queryset):
        items_list = []
        logger.debug("queryset received: %s", queryset)
        for item in queryset:
#            logger.debug("item: %s", list(item.values())[0])
            items_list.append(list(item.values())[0])

#        logger.debug("items_list: %s", items_list)
        return items_list


