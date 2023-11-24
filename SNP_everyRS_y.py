import pandas as pd
import numpy as np
def calculate_intermarriage_count(marriage_rate, group1, group2):
    possible_marriages_from_group1 = group1 * marriage_rate
    possible_marriages_from_group2 = group2 * marriage_rate
    return min(possible_marriages_from_group1, possible_marriages_from_group2)

#
def calculate_snp_evolution(population_end, number_of_births, number_imported, black_population_list,
                            white_population_list, african_snp, european_snp, target_snp, generation_time=20):
    """
        Calculates the evolution of SNP (Single Nucleotide Polymorphism) in the African American population over generations.

        This function simulates the change in SNP of the African American population over time, considering factors such as
        interracial and intraracial marriages, birth rates, and the introduction of new SNPs through slavery and other means.

        Parameters:
        population_end (list): List of population sizes at the end of each generation.
        number_of_births (list): Number of births in each generation.
        number_imported (list): Number of individuals imported (e.g., through slavery) in each generation.
        black_population_list (list): Population size of African Americans in each generation.
        white_population_list (list): Population size of European Americans in each generation.
        african_snp (float): Initial SNP value for African population.
        european_snp (float): Initial SNP value for European population.
        target_snp (float): Target SNP value for the African American population.
        generation_time (int, optional): Average time span of one generation. Default is 20 years.

        Returns:
        tuple: Two lists containing the years and corresponding SNP values for each generation.
        """

    african_american_snp = african_snp  # Initial SNP of African American
    interracial_marriage_rate = 0.086
    african_snp = african_snp
    european_snp = european_snp
    birth_rate = 1.8
    # intraracial_marriage_rate = 0.942
    male_female_ratio = 1.04/(1.04+1)
    generations = 0  # Track the number of generations
    years = []
    snps = []

    while african_american_snp < target_snp:
        if generations < len(population_end):
            # Calculate the SNP changes due to interracial marriages
            # The SNP value for interracial marriages is averaged between the European SNP values in Y chromosome
            snp_interracial_marriage = male_female_ratio*interracial_marriage_rate*number_of_births[generations]*european_snp

            snp_intraracial_marriage = male_female_ratio*(1-interracial_marriage_rate)*number_of_births[generations]*african_american_snp

            snp_slaved = male_female_ratio*number_imported[generations]*african_snp

            remain = male_female_ratio*population_end[generations]-number_of_births[generations]-number_imported[generations]

            if remain>0:
                snp_remain = remain*african_american_snp
                african_american_snp = (snp_slaved+snp_intraracial_marriage+snp_interracial_marriage+snp_remain)/(population_end[generations]*male_female_ratio)
            else:
                african_american_snp = (snp_slaved + snp_intraracial_marriage + snp_interracial_marriage) / (population_end[generations]*male_female_ratio)
        else:
            total_black = black_population_list[generations-len(population_end)-1]
            total_white = white_population_list[generations-len(population_end)-1]

            interracial_marriage_children_number = male_female_ratio*birth_rate * calculate_intermarriage_count(interracial_marriage_rate,
                                                                                              total_black, total_white)

            snp_interracial_marriage = interracial_marriage_children_number * european_snp

            intraracial_marriage_rate_children_number = male_female_ratio*birth_rate * calculate_intermarriage_count((1-interracial_marriage_rate), total_black, total_black)

            snp_intraracial_marriage = intraracial_marriage_rate_children_number * african_american_snp

            new_snp = (snp_intraracial_marriage + snp_interracial_marriage + total_black*african_american_snp) / ((
                        total_black + interracial_marriage_children_number + intraracial_marriage_rate_children_number)*male_female_ratio)

            african_american_snp = new_snp

        generations = generations + 1
        year = generations * generation_time + 1620
        years.append(year)
        snps.append(african_american_snp)

    return years, snps


population_end = [585, 2862, 6832, 27806, 67294, 156040, 247027, 459446, 706514, 1195182, 2021968, 3204420]
number_of_births = [59, 704, 2276, 9281, 29159, 83466, 213185, 350617, 685098, 1343163, 2284539, 3405718]
number_imported = [260, 1636, 6620, 13144, 34064, 107006, 30960, 100686, 41418, 82578, 1501, 303]


black_population_list = [11460802, 16322670, 18661757, 20291124, 21334604, 24756561, 30811352, 34080569,
                         40582096, 53481390, 50084539, 56641508, 64844150, 64584285]

white_population_list = [77092347, 121910454, 176552872, 205107660, 253773760, 336951953, 366490843,
                         388057692, 411146696, 434013891, 427830538]

def find_nearest_below(value, data_list):
    """
    Returns the closest value in data_list that is less than the given value.
    If not found, returns None.
    """
    below_values = [v for v in data_list if v < value]
    if below_values:
        return max(below_values)
    else:
        return None


def linear_interpolation(x, x0, x1, y0, y1):
    return y0 + (x - x0) * (y1 - y0) / (x1 - x0)

def fill_data(full_years, orginial_years, data):
    """Populates data for the given list of years."""
    filled_data = []
    for year in full_years:
        if year in orginial_years:
            filled_data.append(data[orginial_years.index(year)])

        else:
            x0 = find_nearest_below(year, orginial_years)
            y0 = data[orginial_years.index(x0)]

            x1 = find_nearest_below(year, orginial_years) + 20
            y1 = data[orginial_years.index(x1)]
            filled_data.append(linear_interpolation(year, x0, x1, y0, y1))

    return filled_data


def find_threshold_year(years_list, data_list, threshold):
    # Loop through the list of data to find the first year that exceeds the threshold
    for i, val in enumerate(data_list):
        if val >= threshold:
            return years_list[i]
    return None  # If no data exceeds the threshold, None is returned

file_path = 'data/processed_SNP_result y.xlsx'
df = pd.read_excel(file_path)
generation_years = []
for i in range(len(df['SNP id'])):
    SNP_id = df['SNP id'][i]
    print(SNP_id)
    target_snp = df['ASW'][i]
    african_snp = df['AFR'][i]
    european_snp = df['EUR'][i]

    snp_years_list, snp_list = calculate_snp_evolution(population_end, number_of_births, number_imported,
                                                       black_population_list, white_population_list,
                                                       african_snp, european_snp, target_snp)
    print(snp_years_list, snp_list)

    full_snp_years_list = np.arange(snp_years_list[0], snp_years_list[-1] + 1)

    filled_snp_list = fill_data(full_snp_years_list, snp_years_list, snp_list)

    target_year = find_threshold_year(full_snp_years_list, filled_snp_list, target_snp)
    print(target_year)
    generation_year = target_year - 1620
    generation_years.append(generation_year)

df['generation year'] = generation_years

# Save the modified DataFrame back to Excel
df.to_excel('Result_test_' + file_path, index=False)
