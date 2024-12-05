from tool_fold.Router import Router, DataStrategyEnum
from outils import outils
from accueil import accueil
from tool_fold.pomodoro import pomodoro
from tool_fold.simple_editeur import simple_editeur
from tool_fold.todo import todo
from tool_fold.markdown_editor import markdown_editor
from communaute import communaute
#from tool_fold.doc import doc

router = Router(DataStrategyEnum.QUERY)

router.routes = {
  "/": accueil,
  "/outil": outils,
  "/pomodoro": pomodoro,
  "/simple_editeur": simple_editeur,
  "/todo": todo,
  "/markdown_editor": markdown_editor,
  "/communaute": communaute
  #"/doc": doc
}