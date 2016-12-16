import pickle
import pandas as pd
import numpy as np
import scipy.stats as stat
from sklearn.feature_extraction.text import CountVectorizer
import sys
import numpy.matlib

######## load the data
# raw_data = pd.read_pickle('cfpb.pickle')
# cfpb_d = pd.read_pickle('cfpb_daily_clean.pickle')
complaint_data = pd.read_pickle('complaint_data.pickle')
num_complaints = complaint_data['Consumer complaint narrative'].shape[0]
big_pickle = pd.read_pickle('Big_Pickle.pickle')
complaint_data['int_index'] = range(0, num_complaints)
np.random.seed(1234)
#### Tagger Words
pop = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'PRP$', 'RB', 'RBR', 'RBS', 'VB',
       'VBD', 'VBN', 'VBP', 'VBZ', 'JJ', 'JJR', 'JJS']

# AWS****
# java_path = '~/cme238-project/jdk/jdk1.8.0_111/bin/java'

# os.environ['JAVAHOME'] = java_path

# wrk_dir = '/Users/jacobperricone/Desktop/STANFORD/stanford-postagger-full-2015-12-09/'

# wrk_dir = '/Users/Blake/Documents/a16/cme238/stanford-postagger-full-2015-12-09/'


###### Farmshare *
# # wrk_dir = '/farmshare/user_data/bmj/cme238-project/stanford-postagger-full-2015-12-09/'
# # AWS *
# # wrk_dir = '/home/ubuntu/cme238-project/stanford-postagger-full-2015-12-09/'
# os.environ['STANFORD_PARSER'] = wrk_dir
# os.environ['STANFORD_MODELS'] = wrk_dir + 'models'
# jar = wrk_dir + 'stanford-postagger.jar'
# # model = wrk_dir + 'models/english-bidirectional-distsim.tagger'
# model = wrk_dir + 'models/english-caseless-left3words-distsim.tagger'

top_ten = ['JPMorgan Chase & Co.',
           'Experian',
           'The Western Union Company',
           'Nationstar Mortgage',
           'Citibank',
           'Bank of America',
           'Wells Fargo & Company',
           'Equifax',
           'Ocwen',
           'Coinbase, Inc.',
           'Encore Capital Group',
           'Capital One',
           'Navient Solutions, Inc.',
           'Empowerment Ventures, LLC',
           'Enova International, Inc.',
           'TransUnion Intermediate Holdings, Inc.']

banks = list(complaint_data['Company'].value_counts().index)
top_banks = [x for x in banks if x in top_ten]
products = list(complaint_data['Product'].value_counts().index)
issues = list(complaint_data['Product'].value_counts().index)
columns = list(complaint_data.columns)


# fetch the indices of data_frame corresponding to a product name
def fetch_indices(filters):
    query = []
    for col_name, col_values in filters.iteritems():
        query.append('(' + ' | '.join(
            ['(' + str(col_name) + '==' + '"' + str(col_values[x]) + '"' + ')' for x in range(len(col_values))]) + ')')

    query = ' & '.join(query)
    idx = complaint_data.query(query)['int_index']
    return idx


## append a column of series to complaint_data with tagged words, repickle it

# For col_name  in col_names in dataframe, bucket each column by unique value. Append a columnn to the complaint data  indicating
# what bucket the complaint falls in
def bucket_by_columns(col_names, dataframe):
    for col_name in col_names:
        # Find the frequency for all unique values of col_name
        bucket_counts = dataframe[col_name].value_counts()
        buckets = list(bucket_counts.index)
        num_buckets = len(buckets)
        dict_buckets = {buckets[i]: i for i in range(num_buckets)}
        dataframe[col_name + '_bucket'] = dataframe[col_name].apply(lambda x: dict_buckets[x])
    return dataframe


# run em algorithm
def em(tfdf, date_vec, entities_vec, num_defects, tolerance, max_iter, min_iter):
    # length of sample
    sample_size = tfdf.shape[0]

    # initialize defect priors
    # defect_priors = np.ones((num_defects,1)) / num_defects
    defect_priors = np.random.dirichlet(np.ones(num_defects), size=1).T

    # initialize random word posteriors for each symptom
    word_probabilites = tfdf.toarray().sum(0).astype('float') / tfdf.toarray().sum(0).sum(0)
    w_post = np.matlib.repmat(word_probabilites.T, num_defects, 1)

    # initialize random mu and sigma for date for each defect
    mu = list(np.random.uniform(min(date_vec), max(date_vec), num_defects))
    sigma = [np.std(date_vec) * 10 for x in range(num_defects)]

    # initialize random seeds
    # issue_posteriors = np.ones((num_defects, num_issues)) / num_issues
    entity_posteriors = []
    for entity in entities_vec.values():
        tmp = np.random.random((num_defects, entity.value_counts().shape[0]))
        entity_posteriors.append(tmp)

        # issue_posteriors = np.random.random((num_defects,num_issues))

        # product_posterior = np.ones((num_defects, num_products)) / num_products
        # product_posterior = np.random.random((num_defects, num_products))

    # initialize defect poseteriors
    defect_posteriors = np.zeros((num_defects, sample_size))
    m = np.zeros((1, sample_size))
    k = 11
    # initialize max of posteriors variables

    # initialize likely hood
    ll_old = -np.infty

    for iter in range(max_iter):
        # e step
        print "Iteration: %d" % (iter + 1)

        # initialize p(x_i | d_j)
        log_xi_posteriors = np.zeros((num_defects, sample_size))
        z = np.zeros((num_defects, sample_size))
        # for every complaint
        for i in range(sample_size):

            # For every Defect
            for j in range(num_defects):
                # Assume conditional independence of entities of complaint, calculate log(p(x_i|d_j))  for each defec
                for entity_post, entity in zip(entity_posteriors, entities_vec.values()):
                    log_xi_posteriors[j, i] = log_xi_posteriors[j, i] + np.log(entity_post[j, entity[i]])

                log_xi_posteriors[j, i] = log_xi_posteriors[j, i] + \
                                          np.sum(np.multiply(tfdf[i, :].toarray()[0], np.log(w_post[j, :]))) \
                                          + np.log(stat.norm(loc=mu[j], scale=sigma[j]).pdf(date_vec[i]))


                # Calculate the posterior p(d_j | x_i) for each defect. Since p(x_i | d_j) is unstable, convert to logspace:
                # p(d_j|x_i) = \frac{ p(d_j) \prod_(x_i | d_j)}{ \sum_l p(d_l) \prod_(x_i | d_l)
                # Now in log space let:  p(d_j |x_i)  -  \frac{e^{z_j}}{\sum_l e^z_l} \rightarrow e^{z_j}
                # where z = \begin{bmatrix} z_1, \vdots, z_j \end{bmatrix}  is defined below:
            z[:, i] = np.log(defect_priors[:, 0]) + log_xi_posteriors[:, i]

            # Step 2: Since e^z_j is unstable so  bound by m = max_j z_j

            m[0, i] = np.amax(z[:, i], 0)
            # Step 3: Now Find indices where z_j - m < -k  (k threshold = 10)
            zero_indices = np.where(z[:, i] - m[0, i] < -k)
            # if len(zero_indices[0]) > 0:
            # print "Had to zero %s posteriors: " % (len(zero_indices[0]))
            non_zero_indices = np.where(z[:, i] - m[0, i] > -k)

            # Step 4: calculate:
            #  \begin{cases} p(d_{j} | x_i) == 0 \mbox{ if } j \in \mbox{ zero indices} \\
            #  p(d_{j} | x_i) = e^{z_j - m}/ \sum_{k \in non_zero} e^{z_k - m} \end{cases}

            # initialize the zero elements
            tmp_dj = np.zeros(z[:, i].shape)

            # calculate the denominator for non zero case



            tmp_zj = np.exp(z[non_zero_indices, i] - m[0, i] * np.ones(z[non_zero_indices, i].shape))
            denominator = np.sum(tmp_zj)

            tmp_dj[non_zero_indices] = tmp_zj / denominator

            # Save the posteriors for complaint i

            defect_posteriors[:, i] = tmp_dj

            ##### Calculate new log likelihood L:
            # L = \sum_i log( \sum_j p(d_j) p(x_i |d_j)) = \sum_i log( \sum_j e^{z_{j}^i} )
            # Now to avoid underflow, for a given complaint let:
            # log(\sum_j e^{z_j}) = log(e^{m} \sum_j e^{z_j - m}) \approx m + ln( \sum_{l: z_l - m >= k} e^{z_l - m}
            # L = \sum_i m_i + log( \sum_{l: z_l - m >=k} e^{z_l - m}
            # I am going to use loops to be explicit and make sure its right:
        ll_new = 0
        for i in range(sample_size):
            ll_new = ll_new + m[0, i]
            tmp = 0
            for j in range(num_defects):
                if z[j, i] - m[0, i] > -k:
                    tmp = tmp + np.exp(z[j, i] - m[0, i])
            if tmp != 0:
                ll_new = ll_new + np.log(tmp)

        if round(ll_new, 1) < round(ll_old, 1):
            print "\n ----LIKELIHOOD NOT INCREASING. LL_old = %s \t LL_new = %s--------\n" % (ll_old, ll_new)
        else:
            print " New Log Likelihood is %s:" % (ll_new)
        # m step

        # Laplace smoothing constant \lambda
        lam = 1
        print "Completing M Step "
        for j in range(num_defects):
            # update the words
            # print 'Doing Defect %d' % (j)

            for i in range(w_post.shape[1]):
                numerator = lam * 1 + np.sum(np.multiply(defect_posteriors[j, :], tfdf[:, i].toarray()[:, 0]))
                denominator = lam * tfdf.shape[1] + np.sum(np.multiply(defect_posteriors[j, :], tfdf.toarray().sum(1)))
                # print "Difference in word post %f " % (w_post[j, i] - numerator / denominator)
                w_post[j, i] = numerator / denominator

            # update the issues
            print "updating entities"
            for k, (entity_post, entity) in enumerate(zip(entity_posteriors, entities_vec.values())):
                numerator = 0
                for i in range(entity_post.shape[1]):
                    numerator = 1 + np.sum(np.multiply(defect_posteriors[j, :], entity == i))
                    denominator = entity_post.shape[1] + np.sum(defect_posteriors[j, :])
                    # print "Difference in issue post %f " % (issue_posteriors[j, i] -  numerator / denominator)
                    entity_posteriors[k][j, i] = numerator / denominator

            # update the dates
            mu[j] = np.sum(np.multiply(defect_posteriors[j, :], date_vec[:])) / np.sum(defect_posteriors[j, :])
            sigma[j] = np.sum(
                np.multiply(defect_posteriors[j, :], np.square(date_vec - np.matlib.repmat(mu[j], sample_size, 1)))) \
                       / np.sum(defect_posteriors[j, :])

        # update the priors
        # Define an epsilon bound on the prior can be messed with
        epsilon = 1e-10
        tmp_d = np.sum(defect_posteriors, 1) / sample_size

        zero_indices = np.where(tmp_d < 1e-60)
        if len(zero_indices[0]) > 0:
            print "----------- Updating PRIOOOR ----- ",
            print zero_indices
        tmp_d[zero_indices] = epsilon
        defect_priors[:, 0] = tmp_d

        print "Change In LogLikelihood: %f" % np.abs(ll_new - ll_old)
        if np.abs(ll_new - ll_old) < tolerance and iter > min_iter:
            ll_old = ll_new
            break
        ll_old = ll_new
    # return all the important shit
    results = {}
    results['Complaint_Posteriors'] = np.exp(log_xi_posteriors)
    results['Defect_posteriors'] = defect_posteriors
    results['Defect_priors'] = defect_priors
    results['LogLikelihood'] = ll_new
    results['Word_Posteriors'] = w_post
    for i, (key, value) in enumerate(entities_vec.iteritems()):
        results[key + '_Posteriors'] = entity_posteriors[i]

    results['Mean_Date'] = mu
    results['Sigma_Date'] = sigma

    return results


# Return a Term Frequencey matrix
def tf_df(df, idx):
    # cv = CountVectorizer(stop_words=En, min_df=0, lowercase=False, token_pattern=r"\b\w+\b")
    cv = CountVectorizer(stop_words='english', min_df=5)
    words = []

    for x in range(len(idx)):
        x = idx[x]
        try:
            words.append(' '.join([(df.ix[x].index[i] + ' ') * df.ix[x][i] for i in range(len(df.ix[x]))]))
        except (AttributeError, TypeError):
            words.append(' '.join(
                [(df.ix[x].values[0].index[i] + ' ') * df.ix[x].values[0][i] for i in range(len(df.ix[x].values[0]))]))

    tfmatrix = cv.fit_transform(words)
    vocab = cv.get_feature_names()

    return tfmatrix, vocab, words, cv


def filter_data(filters, buckets, percentage=0.0):
    idx = fetch_indices(filters)
    if idx.shape[0] == 0:
        print "No complaints match results"
        return -1
    else:
        if percentage:
            rand_indices = list(np.random.choice(np.arange(0, idx.shape[0]), int(idx.shape[0] * percentage)))
            idx = idx[rand_indices]
            df = complaint_data.ix[idx, columns].reset_index()
            dframe = bucket_by_columns(buckets, df)
        else:
            df = complaint_data.ix[idx, columns].reset_index()
            dframe = bucket_by_columns(buckets, df)
    entities_vec = {}
    for bucket in buckets:
        entities_vec[bucket] = dframe[bucket + '_bucket']

    return dframe, idx, entities_vec


def main():
    # bucket by company, product, and issue

    num_defects = int(sys.argv[1])
    banks = list(complaint_data['Company'].value_counts().index)
    top_banks = [x for x in banks if x in top_ten]
    products = list(complaint_data['Product'].value_counts().index)
    top_products = list(complaint_data['Product'].
                        value_counts().index[0:6])
    issues = list(complaint_data['Issue'].value_counts().index)
    columns = list(complaint_data.columns)

    # orig indices can be gotten by idx[i]
    union_top_companies = set()
    for product in top_products:
        companies = list(complaint_data[complaint_data['Product'] == product]['Company'].value_counts().index[1:10])
        union_top_companies |= set(companies)

    filters = {'Company': list(union_top_companies), 'Product': top_products}
    buckets = ['Issue', 'Company', 'Product']

    df, idx, entities_vec = filter_data(filters, buckets,0.0)
    issues = list(df['Issue'].value_counts().index)
    products = list(df['Product'].value_counts().index)
    banks = list(df['Company'].value_counts().index)
    date_vec = [float(x) for x in list(idx.index.astype(np.int64))]
    symptom_vec = big_pickle.ix[idx]
    tfdf, vocab, words, cv = tf_df(symptom_vec, idx)

    tol = 1e-4
    max_iter = 10000
    min_iter = 0

    print num_defects

    results = em(tfdf, date_vec, entities_vec, num_defects, tol, max_iter, min_iter)
    results['vocab'] = vocab
    pickle.dump(results, open("Big_EM_Date_" + str(num_defects) + '.pickle', "wb"))
    #
    # entities_dict= {'Issue_Posteriors': issues, 'Company_Posteriors':list(union_top_companies), 'Product_Posteriors':top_products}
    # top_per_entity = {}
    # for bucket in buckets:
    #     bucket = bucket + '_Posteriors'
    #     top_per_entity[bucket + '_Posteriors'] = {'Defect ' + str(i):[entities_dict[bucket][x]  for x in results[bucket][i,:].argsort()[-2:][::-1]] for i in range(num_defects)}
    # #[issues[x] for x in issue_posteriors[4,:].argsort()[-5:][::-1]]
    # num = 5
    # top_complaints_per_defect = {str(i): list(logx_i_posteriors[i,:].argsort()[-num:][::-1]) for i in range(num_defects)}
    # top_words_per_defect= {str(i): [vocab[x] for x in w_post[i, :].argsort()[-num:][::-1]] for i in range(num_defects)}
    # top_issues_per_defect = {str(i):[issues[x] for x in issue_posteriors[i, :].argsort()[-2:][::-1]] for i in range(num_defects)}
    ##
    # print top_words_per_defect
    # print top_issues_per_defect
    # print top_complaints_per_defect


if __name__ == '__main__':
    main()
