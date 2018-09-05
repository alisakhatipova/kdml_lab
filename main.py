from os import path
from thunderdome import *
from constants import *
from algorithms import *
from sklearn import datasets
import matplotlib.pyplot as plt
import logging
import json
algorithms = [alg_svm, alg_lr, alg_nn]
alg_names = [alg_svm.__name__,  alg_lr.__name__, alg_nn.__name__]


def split_comparison_experiment(X):
    group_size = 2
    model_num = 10
    res_full = {alg: [] for alg in alg_names}
    res_full_baseline = {alg: [] for alg in alg_names}
    res_simple = {alg: [] for alg in alg_names}
    res_simple_baseline = {alg: [] for alg in alg_names}
    res_no = {alg: [] for alg in alg_names}
    res_no_baseline = {alg: [] for alg in alg_names}
    res_real = {alg: [] for alg in alg_names}
    train_time_real = {alg: [] for alg in alg_names}
    train_time_decentr = {alg: [] for alg in alg_names}
    for i in range(ITER_NUM):
        logger.info("ITERATION NUMBER " + str(i) + ' ***************************************************************')
        for alg in algorithms:
            algname = alg.__name__
            # train models (only need to do it once for all experiments
            # compute result and time for decentralized case
            experiment = ThunderDome(X, alg, group_size, model_num, logger,
                                     split_type=SIMPLE_SPLIT)
            tr_time, auc = experiment.run_experiment()
            train_time_decentr[algname].append(tr_time)
            res_simple[algname].append(auc)
            tr_time, auc = experiment.compute_real_result()
            train_time_real[algname].append(tr_time)
            res_real[algname].append(auc)

            # baseline SIMPLE SPLIT
            experiment = ThunderDome(X, alg, model_num, model_num, logger,
                                     split_type=SIMPLE_SPLIT, need_to_retrain=False)
            _, auc = experiment.run_experiment()
            res_simple_baseline[algname].append(auc)

            # the same experiment for FULL_SPLIT
            experiment = ThunderDome(X, alg, group_size, model_num, logger,
                                     split_type=FULL_SPLIT, need_to_retrain=False)
            _, auc = experiment.run_experiment()
            res_full[algname].append(auc)

            # baseline FULL SPLIT
            experiment = ThunderDome(X, alg, model_num, model_num, logger,
                                     split_type=FULL_SPLIT, need_to_retrain=False)
            _, auc = experiment.run_experiment()
            res_full_baseline[algname].append(auc)

            # the same experiment for NO_SPLIT
            experiment = ThunderDome(X, alg, group_size, model_num, logger,
                                     split_type=NO_SPLIT, need_to_retrain=False)
            _, auc = experiment.run_experiment()
            res_no[algname].append(auc)

            # baseline NO SPLIT
            experiment = ThunderDome(X, alg, model_num, model_num, logger,
                                     split_type=NO_SPLIT, need_to_retrain=False)
            _, auc = experiment.run_experiment()
            res_no_baseline[algname].append(auc)
    with open(path.join(LOG_FOLDER, 'split_comparison_experiment'), 'w') as out:
        for alg in alg_names:
            aver_real = sum(res_real[alg]) * 1.0 / ITER_NUM
            res = alg + '_res_real = ' + json.dumps(res_real[alg]) + '\n' + alg + '_aver_real = ' + str(aver_real) + '\n'
            out.write(res)

            aver_full = sum(res_full[alg]) * 1.0 / ITER_NUM
            res = alg + '_res_full = ' + json.dumps(res_full[alg]) + '\n' +alg +  '_aver_full = ' + str(aver_full) + '\n'
            out.write(res)
            aver_full_baseline = sum(res_full_baseline[alg]) * 1.0 / ITER_NUM
            res = alg + '_res_full_baseline = ' + json.dumps(res_full_baseline[alg]) + '\n' + alg + '_aver_full_baseline = ' + str(aver_full_baseline) + '\n'
            out.write(res)

            aver_simple = sum(res_simple[alg]) * 1.0 / ITER_NUM
            res = alg + '_res_simple = ' + json.dumps(res_simple[alg]) + '\n' + alg + '_aver_simple = ' + str(aver_simple) + '\n'
            out.write(res)
            aver_simple_baseline = sum(res_simple_baseline[alg]) * 1.0 / ITER_NUM
            res = alg + '_res_simple_baseline = ' + json.dumps(res_simple_baseline[alg]) + '\n' + alg + '_aver_simple_baseline = ' + str(aver_simple_baseline) + '\n'
            out.write(res)

            aver_no = sum(res_no[alg]) * 1.0 / ITER_NUM
            res =alg +  '_res_no = ' + json.dumps(res_no[alg]) + '\n' + alg + '_aver_no = ' + str(aver_no) + '\n'
            out.write(res)
            aver_no_baseline = sum(res_no_baseline[alg]) * 1.0 / ITER_NUM
            res = alg + '_res_no_baseline = ' + json.dumps(res_no_baseline[alg]) + '\n' + alg + '_aver_no_baseline = ' + str(aver_no_baseline) + '\n'
            out.write(res)

            aver_time_decentr = sum(train_time_decentr[alg]) * 1.0 / ITER_NUM
            res = alg + '_train_time_decentr = ' + json.dumps(train_time_decentr[alg]) + '\n' + alg + '_aver_train_time_decentr = ' + str(aver_time_decentr) + '\n'
            out.write(res)

            aver_time_real = sum(train_time_real[alg]) * 1.0 / ITER_NUM
            res = alg + '_train_time_real = ' + json.dumps(train_time_real[alg]) + '\n' + alg + '_aver_train_time_real = ' + str(aver_time_real) + '\n'
            out.write(res)


def group_size_comparison_experiment(X):
    group_sizes = [2, 5]
    model_num = 10
    res_real = {alg: {gr_size: [] for gr_size in group_sizes} for alg in alg_names}
    res_normal = {alg: {gr_size: [] for gr_size in group_sizes} for alg in alg_names}
    res_baseline = {alg: {gr_size: [] for gr_size in group_sizes} for alg in alg_names}

    for i in range(ITER_NUM):
        logger.info(
            "ITERATION NUMBER" + str(i) + ' ***************************************************************')
        for alg in algorithms:
            for group_size in group_sizes:
                algname = alg.__name__
                experiment = ThunderDome(X, alg, group_size, model_num, logger,
                                         split_type=SIMPLE_SPLIT)
                _, auc = experiment.run_experiment()
                res_normal[algname][group_size].append(auc)
                _, auc = experiment.compute_real_result()
                res_real[algname][group_size].append(auc)
                # baseline
                experiment = ThunderDome(X, alg, model_num, model_num, logger,
                                         split_type=SIMPLE_SPLIT, need_to_retrain=False)
                _, auc = experiment.run_experiment()
                res_baseline[algname][group_size].append(auc)

    with open(path.join(LOG_FOLDER, 'group_size_comparison_experiment'), 'w') as out:
        for alg in alg_names:
            for group_size in group_sizes:
                gr = str(group_size)
                aver_real = sum(res_real[alg][group_size]) * 1.0 / ITER_NUM
                res = alg + gr +'_res_real = ' + json.dumps(res_real[alg][group_size]) + '\n' + alg+ gr + '_aver_real = ' + str(aver_real) + '\n'
                out.write(res)

                aver_normal = sum(res_normal[alg][group_size]) * 1.0 / ITER_NUM
                res = alg+ gr + '_res_normal = ' + json.dumps(res_normal[alg][group_size]) + '\n' +alg+ gr +  '_aver_normal = ' + str(aver_normal) + '\n'
                out.write(res)
                aver_baseline = sum(res_baseline[alg][group_size]) * 1.0 / ITER_NUM
                res = alg+ gr + '_res_baseline = ' + json.dumps(res_baseline[alg][group_size]) + '\n' + alg + gr+ '_aver_baseline = ' + str(aver_baseline) + '\n'
                out.write(res)


def learners_num_comparison_experiment(X):
    models_nums = [5, 10]
    group_size = 5
    res_real = {alg: {model_num: [] for model_num in models_nums} for alg in alg_names}
    res_normal = {alg: {model_num: [] for model_num in models_nums} for alg in alg_names}
    res_baseline = {alg: {model_num: [] for model_num in models_nums} for alg in alg_names}
    for i in range(ITER_NUM):
        logger.info(
            "ITERATION NUMBER " + str(i) + ' ***************************************************************')
        for alg in algorithms:
            for model_num in models_nums:
                algname = alg.__name__
                experiment = ThunderDome(X, alg, group_size, model_num, logger,
                                         split_type=SIMPLE_SPLIT)
                _, auc = experiment.run_experiment()
                res_normal[algname][model_num].append(auc)
                _, auc = experiment.compute_real_result()
                res_real[algname][model_num].append(auc)
                # baseline
                experiment = ThunderDome(X, alg, model_num, model_num, logger,
                                         split_type=SIMPLE_SPLIT, need_to_retrain=False)
                _, auc = experiment.run_experiment()
                res_baseline[algname][model_num].append(auc)

            with open(path.join(LOG_FOLDER, 'model_num_comparison_experiment'), 'w') as out:
                for alg in alg_names:
                    for model_num in models_nums:
                        mn = str(model_num)
                        aver_real = sum(res_real[alg][model_num]) * 1.0 / ITER_NUM
                        res = alg + mn + '_res_real = ' + json.dumps(
                            res_real[alg][model_num]) + '\n' + alg + mn + '_aver_real = ' + str(aver_real) + '\n'
                        out.write(res)

                        aver_normal = sum(res_normal[alg][model_num]) * 1.0 / ITER_NUM
                        res = alg + mn + '_res_normal = ' + json.dumps(
                            res_normal[alg][model_num]) + '\n' + alg + mn + '_aver_normal = ' + str(aver_normal) + '\n'
                        out.write(res)
                        aver_baseline = sum(res_baseline[alg][model_num]) * 1.0 / ITER_NUM
                        res = alg + mn + '_res_baseline = ' + json.dumps(
                            res_baseline[alg][model_num]) + '\n' + alg + mn + '_aver_baseline = ' + str(
                            aver_baseline) + '\n'
                        out.write(res)


if __name__ == "__main__":
    try:
        os.stat(LOG_FOLDER)
    except:
        os.mkdir(LOG_FOLDER)

    try:
        os.stat(MODELS_FOLDER)
    except:
        os.mkdir(MODELS_FOLDER)

    log_file = path.join(LOG_FOLDER, 'log.txt')
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    np.random.seed(0)
    logger = logging.getLogger()
    # X = np.loadtxt('datasets/SUSY.csv', dtype='f4', delimiter=',')
    # classes = X[:, 0].reshape((-1, 1))
    # all_set = X[:, 1:]
    # idx = np.random.permutation(len(all_set))
    # all_set = all_set[idx]
    # classes = classes[idx]
    all_set, classes = datasets.load_breast_cancer(return_X_y=True)
    positive_samples = all_set[np.where(classes == 1)[0]]
    negative_samples = all_set[np.where(classes == 1)[0]]
    # all_set, classes = self.shuffle_data(all_set, classes)
    X = [positive_samples, negative_samples]

    # learners_num_comparison_experiment(X)



    # X = np.loadtxt('datasets/SUSY.csv', dtype='f4', delimiter=',')
    # np.random.seed(34445)
    # classes = X[:, 0].reshape((-1, 1))
    # all_set = X[:, 1:]
    # idx = np.random.permutation(len(all_set))
    # all_set = all_set[idx]
    # classes = classes[idx]
    # all_set = np.array_split(all_set, 10)[0]
    # classes = np.array_split(classes, 10)[0]
    # np.savetxt('datasets/data10.csv', all_set, delimiter=',')
    # np.savetxt('datasets/classes10.csv', classes,  delimiter=',')
    # all_set = np.array_split(all_set, 1000)[0]
    # classes = np.array_split(classes, 1000)[0]