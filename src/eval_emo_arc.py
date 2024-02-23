from scipy.stats import spearmanr
import csv
from collections import OrderedDict
import math
import statistics as stat
from sklearn.metrics import mean_squared_error

class FindCorrelation:
    def __init__(self, manual_filename, automatic_filename, bin_size):
        self.manual_filename = manual_filename
        self.automatic_filename = automatic_filename
        self.aut_tweet_score = self.extractAutomatic(self.automatic_filename)
        self.man_tweet_score = self.extractManual(self.manual_filename)
        return 

    def extractManual(self, filename):
        tweet_score = OrderedDict()
        lines = open(filename, "r").readlines()
        
        for line in lines[1:]:
            prts = line.strip().split("\t")
            tweet = prts[1]
            score = float(prts[3])
            tweet_score = score
            
        return tweet_score

    def extractAutomatic(self, filename):
        tweet_score = OrderedDict()
        with open(filename) as csvfile:
            tweet_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            header = next(tweet_reader)
            for row in tweet_reader:
                tweet = row[header.index('text')]
                score = row[header.index('avgLexVal')]
                if score != "NA":
                    score = float(score)
                
                tweet_score[tweet] = score
        return tweet_score
    
    def Standardize(self, lst):
        if len(lst) == 0:
            return None
        sum = 0
        cnt = 0
        no_NA_lst = []
        for item in lst:
            if item != "NA":
                sum += item
                cnt += 1
                no_NA_lst.append(item)
        avg = sum/cnt
        std_dev = stat.stdev(no_NA_lst)
        if std_dev == 0:
            return None
        new_lst = []
        for item in no_NA_lst:
            y = (item-avg)/std_dev
            new_lst.append(y)
        
        return new_lst
    
    def calcScore_withoutNAbins(self, all_man, all_aut, bin_size):
        avg_man = []
        avg_aut = []
        
        if all_man != None and all_aut != None:
            for i in range(len(all_man) - bin_size + 1):
                window_man = all_man[i: i + bin_size]
                window_aut = all_aut[i: i + bin_size]
                sum_aut = 0
                cnt_aut = 0
                for item in window_aut:
                    if item != "NA":
                        sum_aut += item
                        cnt_aut += 1
                if cnt_aut != 0:
                    avg_aut.append(sum_aut/cnt_aut)
                    avg_man.append(sum(window_man)/bin_size)
            return avg_man, avg_aut
        else:
            return [], []
    
    def RollingWindow(self, man_tweet_score, aut_tweet_score, bin_size, removeNA):
        all_man = []
        all_aut = []

        man_tweet_score = OrderedDict(sorted(man_tweet_score.items(), key=lambda item: item[1]))
        for tweet in sorted(man_tweet_score, key=man_tweet_score.get):
            score = man_tweet_score[tweet]
            if tweet in aut_tweet_score.keys():
                all_man.append(score)
                all_aut.append(aut_tweet_score[tweet])

        if removeNA:
            avg_man, avg_aut = self.calcScore_withoutNAbins(all_man, all_aut, bin_size)
        else:
            avg_man = []
            avg_aut = []

            for i in range(len(all_man) - bin_size + 1):
                avg_man.append(sum(all_man[i: i + bin_size])/bin_size)
                avg_aut.append(sum(all_aut[i: i + bin_size])/bin_size)

        num_unique_aut = len(set(avg_aut))
        num_unique_man = len(set(avg_man))

        avg_man_stand = self.Standardize(avg_man)
        avg_aut_stand = self.Standardize(avg_aut)
        
        if len(avg_man) < 2 or len(avg_aut) < 2:
            return None, None, len(avg_man), num_unique_aut, num_unique_man, avg_man_stand, avg_aut_stand
        
        if avg_man_stand == None or avg_aut_stand == None:
            return None, None, len(avg_man), num_unique_aut, num_unique_man, None, None

        MSE = mean_squared_error(avg_man_stand, avg_aut_stand)
        RMSE = math.sqrt(MSE)

        correlation_s_stand, p_value = spearmanr(avg_man_stand, avg_aut_stand)

        return RMSE, correlation_s_stand, len(avg_man), num_unique_aut, num_unique_man, avg_man_stand, avg_aut_stand


def runExp(emotions, lexicon_type, automatic_output_dir, manual_annotation_filename, bin_sizes, na_present, na_score, dataset_name, dataset_type, lang, removeNA):
    for emotion in emotions: 
        automatic_filename = automatic_output_dir + emotion.lower() + ".csv"
        for bin_size in bin_sizes:
            fc = FindCorrelation(manual_annotation_filename, automatic_filename, bin_size)
            
            RMSE, corr_s_stand, length, num_unique_aut, num_unique_man, avg_man_stand, avg_aut_stand = fc.RollingWindow(fc.man_tweet_score, fc.aut_tweet_score, bin_size, removeNA)
            f2.write(dataset_name + "," + dataset_type + "," + lang + "," + emotion + "," + lexicon_type + "," + na_present + "," + na_score + "," + str(bin_size) + "," + str(RMSE) + "," + str(corr_s_stand) + "," + str(length) + "," + str(num_unique_aut) + "," + str(num_unique_man) + "\n")
            writeBinScores(dataset_name, dataset_type, lang, emotion, lexicon_type, na_present, na_score, bin_size, avg_man_stand, avg_aut_stand)
            
    return

def writeBinScores(dataset_name, dataset_type, lang, emotion, lexicon_type, na_present, na_score, bin_size, avg_man_stand, avg_aut_stand):
    if avg_man_stand == None or avg_aut_stand == None:
        return
    else:
        for i in range(len(avg_man_stand)):
            f.write(dataset_name + "," + dataset_type + "," + lang + "," + emotion + "," + lexicon_type + "," + na_present + "," + na_score + "," + str(bin_size) + "," + str(avg_man_stand[i]) + "," + str(avg_aut_stand[i]) + "\n")
    return

if __name__=="__main__":
    rootdir = ""
    
    output_filename_data = "bin_scores.txt"
    f = open(output_filename_data, "w")
    f.write("Test Data,Test Data Type,Lang,Emotion,Lexicon Scores,N/As,OOV,Bin,Manual Bin Score,Automatic Bin Score"+ "\n")

    output_filename = "correlations_all.txt"
    f2 = open(output_filename, "w")
    f.write("Test Data,Test Data Type,Lang,Emotion,Lexicon Scores,N/As,OOV,Bin,RMSE,SpearCorr,LengthArc,NumUniqueAut,NumUniqueMan"+ "\n")

    ########################################################################
    # V-reg
    emotions = ["Valence"]
    lexicon_type = "real-valued"
    automatic_output_dir = ""
    manual_annotation_filename = ""
    bin_sizes = [1,10,50,100,200,300]
    na_present = "none"
    na_score = "assigned neutral score"
    dataset_name = "SemEval 2018 (V-Reg)"
    dataset_type = "continuous"
    lang = "Eng"
    removeNA = False
    runExp(emotions, lexicon_type, automatic_output_dir, manual_annotation_filename, bin_sizes, na_present, na_score, dataset_name, dataset_type, lang, removeNA)

    na_present = "present"
    na_score = "assigned NA"
    removeNA = True
    runExp(emotions, lexicon_type, automatic_output_dir, manual_annotation_filename, bin_sizes, na_present, na_score, dataset_name, dataset_type, lang, removeNA)
    ########################################################################
    
    f2.close()
    f.close()
