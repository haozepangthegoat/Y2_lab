from icecream import ic
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import dpcentre as dp

experiment1 = r'raw_data/ThermalDiffusivity_StepChange_experiment_1.csv'

df = pd.read_csv(experiment1)
ic(df['time'])





