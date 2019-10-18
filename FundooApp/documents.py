

















from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import FundooNotes


@registry.register_document
class FundooNotesDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'notes'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = FundooNotes # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'title',
    'note',
    'reminder',

    'color',
    'image',
    'archieve',
    'is_trash'


        ]


########################################################################################################
########################working code ends there
#
# from django_elasticsearch_dsl.documents import DocType
# from django_elasticsearch_dsl import Index
#
# from .models import FundooNotes
#
#
# posts = Index('posts')
#
#
# @posts.doc_type
# class FundooNotesDocument(DocType):
#
#     class Django:
#         model = FundooNotes
#         fields = [
#             "note",
#         ]




# from django_elasticsearch_dsl import  Index
# from django_elasticsearch_dsl.documents import DocType
# from .models import FundooNotes
#
# posts = Index('posts')
#
# @posts.doc_type
# class PostDocument(DocType):
#     class Django:
#         model = FundooNotes
#
#         fields = [
#             'title',
#             'note',
#             'reminder',
#         ]


# from elasticsearch_dsl import analyzer
#
# from django_elasticsearch_dsl import  Index, fields
# from django_elasticsearch_dsl.documents import DocType
# from .models import FundooNotes
#
# Fundoo_index = Index('notes')
# Fundoo_index.settings(
#     number_of_shards=1,
#     number_of_replicas=0
# )
#
# html_strip = analyzer(
#     'html_strip',
#     tokenizer="standard",
#     filter=["standard", "lowercase", "stop", "snowball"],
#     char_filter=["html_strip"]
# )
#
#
#
# @Fundoo_index.doc_type
# class FundooNotesDocument(DocType):
#     """Article elasticsearch document"""
#
#     id = fields.IntegerField(attr='id')
#     title = fields.StringField(
#         analyzer=html_strip,
#         fields={
#             'raw': fields.StringField(analyzer='keyword'),
#         }
#     )
#     notes = fields.TextField(
#         analyzer=html_strip,
#         fields={
#             'raw': fields.TextField(analyzer='keyword'),
#         }
#     )
#     reminder = fields.DateField()
#
#     # author = fields.IntegerField(attr='author_id')
#     # created = fields.DateField()
#     # modified = fields.DateField()
#
#     class Meta:
#         model = FundooNotes