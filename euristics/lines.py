import numpy as np

from allLibs import *


def lines(analyzer1_info, analyzer2_info, eur_params):

    name_catalog1 = [warn[0] for warn in count_warnings(analyzer1_info)]
    name_catalog2 = [warn[0] for warn in count_warnings(analyzer2_info)]

    name_catalog1.append("ONLY_IN_ANALYZER2")
    name_catalog1.append("TOTAL_AMOUNT_AN2")

    name_catalog2.append("ONLY_IN_ANALYZER1")
    name_catalog2.append("TOTAL_AMOUNT_AN1")

    stat_matrix = np.zeros((len(name_catalog1), len(name_catalog2)), dtype="int")
    stat_matrix[-1][-1] = -1
    stat_matrix[-1][-2] = -1
    stat_matrix[-2][-1] = -1
    stat_matrix[-2][-2] = -1


    error_list_both = []
    error_list_an1 = []
    error_list_an2 = []

    cmp_list = []

    found_counterpart_an2 = np.zeros((len(analyzer2_info)), dtype=np.bool)
    for defect1_file_ind in range(len(analyzer1_info)):
        found_counterpart_an1 = False

        for err_ind in range(len(analyzer1_info[defect1_file_ind][2])):
            # print([srch_ind(name_catalog1, [analyzer1_info[defect1_file_ind][2][err_ind]])])
            stat_matrix[srch_list_ind(name_catalog1, analyzer1_info[defect1_file_ind][2][err_ind])][-1] += 1

        for defect2_file_ind in range(len(analyzer2_info)):
            if analyzer1_info[defect1_file_ind][0] == analyzer2_info[defect2_file_ind][0]:
                cmp_list.append([analyzer1_info[defect1_file_ind][0],
                                 analyzer1_info[defect1_file_ind][1],
                                 analyzer2_info[defect2_file_ind][1],
                                 analyzer1_info[defect1_file_ind][2],
                                 analyzer2_info[defect2_file_ind][2]])

                found_counterpart_an1 = True
                found_counterpart_an2[defect2_file_ind] = True
                break

        if not found_counterpart_an1:
            #print(analyzer1_info[defect1_file_ind][2])
            for err_ind in range(len(analyzer1_info[defect1_file_ind][2])):
                #print([srch_ind(name_catalog1, [analyzer1_info[defect1_file_ind][2][err_ind]])])
                stat_matrix[srch_list_ind(name_catalog1, analyzer1_info[defect1_file_ind][2][err_ind])][-2] += 1
                error_list_an1.append([analyzer1_info[defect1_file_ind][0],
                                      analyzer1_info[defect1_file_ind][1][err_ind],
                                      analyzer1_info[defect1_file_ind][2][err_ind]]
                                      )

    for defect2_file_ind2 in range(found_counterpart_an2.shape[0]):

        for err_ind in range(len(analyzer2_info[defect2_file_ind2][2])):
            ind2 = srch_list_ind(name_catalog2, analyzer2_info[defect2_file_ind2][2][err_ind])
            stat_matrix[-1][ind2] += 1

        if not found_counterpart_an2[defect2_file_ind2]:
            for err_ind in range(len(analyzer2_info[defect2_file_ind2][2])):
                ind2 = srch_list_ind(name_catalog2, analyzer2_info[defect2_file_ind2][2][err_ind])
                stat_matrix[-2][ind2] += 1
                error_list_an2.append(analyzer2_info[defect2_file_ind2])

    #################CMP_LIST######################

    for file in cmp_list:
        present_in_an1_ar = np.zeros((len(file[2])), dtype=np.bool)
        for defect1_lines_ind in range(len(file[1])):
            present_in_an2 = False
            error_name1 = file[3][defect1_lines_ind]
            ind1 = srch_list_ind(name_catalog1, error_name1)

            for defect2_lines_ind in range(len(file[2])):

                intersection = []
                for line1 in file[1][defect1_lines_ind]:
                    for line2 in file[2][defect2_lines_ind]:
                        if math.fabs(line2 - line1) <= eur_params["distance"]:
                            intersection.append(line1)

                #intersection = [value for value in file[1][defect1_lines_ind] if value in file[2][defect2_lines_ind]]
                if len(intersection):
                    present_in_an1_ar[defect2_lines_ind] = True
                    error_name2 = file[4][defect2_lines_ind]
                    ind2 = srch_list_ind(name_catalog2, error_name2)

                    present_in_an2 = True
                    stat_matrix[ind1][ind2] += 1
                    error_list_both.append([file[0], intersection, error_name1, error_name2])

            if not present_in_an2:
                stat_matrix[ind1][-2] += 1
                error_list_an1.append([file[0], file[1][defect1_lines_ind], error_name1])

        for analyzer2_warning_ind in range(len(present_in_an1_ar)):
            if not present_in_an1_ar[analyzer2_warning_ind]:
                error_name2 = file[4][analyzer2_warning_ind]
                ind2 = srch_list_ind(name_catalog2, error_name2)
                stat_matrix[-2][ind2] += 1
                error_list_an2.append([file[0], file[2][analyzer2_warning_ind], error_name2])

    return name_catalog1, \
           name_catalog2, \
           stat_matrix, \
           error_list_an1, \
           error_list_an2, \
           error_list_both