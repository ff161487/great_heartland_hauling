import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from pdb import set_trace


def fitting():
    # Loading data
    df = pd.read_feather('ghh.f')
    set_trace()

    # Split X and Y
    mdl = smf.glm('Win ~ Round + C(Action_From) + C(Action_To) + C(Action_N_Steps) + C(Action_Type) +'
                  ' C(Action_Bean) + C(Action_Corn) + C(Action_Pig) + C(Action_Cow) + C(Action_1_Step) +'
                  ' C(Action_2_Steps) + C(Action_3_Steps)', df, family=sm.families.Binomial())
    res = mdl.fit()
    print(res.summary())
    set_trace()


if __name__ == '__main__':
    fitting()
