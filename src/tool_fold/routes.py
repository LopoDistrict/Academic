from tool_fold.Router import Router, DataStrategyEnum
from outils import outils
from accueil import accueil
from tool_fold.pomodoro import pomodoro
#from tool_fold.simple_editeur import simple_editeur
from tool_fold.todo import todo
from tool_fold.markdown_editor import markdown_editor
from tool_fold.flash_cards import flash_cards
from tool_fold.calendar import calendar
from communaute import communaute
from librairie import librairie
from feed import feed
from about import about
from tool_fold.transform_stream import transform_stream
#from tool_fold.doc import doc

router = Router(DataStrategyEnum.QUERY)

router.routes = {
  "/": accueil,
  "/outil": outils,
  "/pomodoro": pomodoro,
  #"/simple_editeur": simple_editeur,
  "/todo": todo,
  "/markdown_editor": markdown_editor,
  "/flash_cards": flash_cards,
  "/communaute": communaute,
  "/librairie": librairie,
  #"/doc": doc,
  "/feed": feed,
  "/about": about,
  "/calendar": calendar,
  "/transform_stream" : transform_stream
}
