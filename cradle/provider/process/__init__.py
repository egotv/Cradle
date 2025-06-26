from cradle.provider.process.action_planning import RDR2ActionPlanningPreprocessProvider
from cradle.provider.process.action_planning import ActionPlanningPreprocessProvider
from cradle.provider.process.action_planning import StardewActionPlanningPreprocessProvider
from cradle.provider.process.action_planning import ActionPlanningPostprocessProvider
from cradle.provider.process.action_planning import RDR2ActionPlanningPostprocessProvider
from cradle.provider.process.action_planning import StardewActionPlanningPostprocessProvider
from cradle.provider.process.information_gathering import RDR2InformationGatheringPreprocessProvider
from cradle.provider.process.information_gathering import InformationGatheringPreprocessProvider
from cradle.provider.process.information_gathering import StardewInformationGatheringPreprocessProvider
from cradle.provider.process.information_gathering import InformationGatheringPostprocessProvider
from cradle.provider.process.self_reflection import RDR2SelfReflectionPreprocessProvider
from cradle.provider.process.self_reflection import SelfReflectionPreprocessProvider
from cradle.provider.process.self_reflection import SelfReflectionPostprocessProvider
from cradle.provider.process.task_inference import TaskInferencePreprocessProvider
from cradle.provider.process.task_inference import TaskInferencePostprocessProvider

# This dictionary maps provider names to their corresponding classes.
__all__ = [
    'RDR2ActionPlanningPreprocessProvider',
    'ActionPlanningPreprocessProvider',
    'StardewActionPlanningPreprocessProvider',
    'ActionPlanningPostprocessProvider',
    'RDR2ActionPlanningPostprocessProvider',
    'StardewActionPlanningPostprocessProvider',
    'RDR2InformationGatheringPreprocessProvider',
    'InformationGatheringPreprocessProvider',
    'StardewInformationGatheringPreprocessProvider',
    'InformationGatheringPostprocessProvider',
    'RDR2SelfReflectionPreprocessProvider',
    'SelfReflectionPreprocessProvider',
    'SelfReflectionPostprocessProvider',
    'TaskInferencePreprocessProvider',
    'TaskInferencePostprocessProvider'
]

# This dictionary maps provider names to their corresponding classes.
providers = {
    'RDR2ActionPlanningPreprocessProvider': RDR2ActionPlanningPreprocessProvider,
    'ActionPlanningPreprocessProvider': ActionPlanningPreprocessProvider,
    'StardewActionPlanningPreprocessProvider': StardewActionPlanningPreprocessProvider,
    'ActionPlanningPostprocessProvider': ActionPlanningPostprocessProvider,
    'RDR2ActionPlanningPostprocessProvider': RDR2ActionPlanningPostprocessProvider,
    'StardewActionPlanningPostprocessProvider': StardewActionPlanningPostprocessProvider,
    'RDR2InformationGatheringPreprocessProvider': RDR2InformationGatheringPreprocessProvider,
    'InformationGatheringPreprocessProvider': InformationGatheringPreprocessProvider,
    'StardewInformationGatheringPreprocessProvider': StardewInformationGatheringPreprocessProvider,
    'InformationGatheringPostprocessProvider': InformationGatheringPostprocessProvider,
    'RDR2SelfReflectionPreprocessProvider': RDR2SelfReflectionPreprocessProvider,
    'SelfReflectionPreprocessProvider': SelfReflectionPreprocessProvider,
    'SelfReflectionPostprocessProvider': SelfReflectionPostprocessProvider,
    'TaskInferencePreprocessProvider': TaskInferencePreprocessProvider,
    'TaskInferencePostprocessProvider': TaskInferencePostprocessProvider
}
