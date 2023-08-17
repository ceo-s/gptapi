# from typing import Literal
# from .llm.preprocessing import Embedder, OverlapOptimizer, TextPreprocessor
# from .db.embedding import _UserCollection

# EMBEDDERS = Literal[

# ]

# OPTIMIZERS = Literal[

# ]

# TextPreprocessor


# class UserCollection(_UserCollection):

#     @classmethod
#     async def acreate(cls, __user_id: int):
#         self = cls()
#         self.__user_id = __user_id
#         await super()._ainit(self, __user_id)
#         return self

#     @classmethod
#     async def from_user(cls, __user_id: int):
#         self = cls()
#         self.__user_id = __user_id
#         await super()._ainit(self, __user_id)
#         return self
