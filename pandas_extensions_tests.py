import unittest
import pandas as pd
import numpy as np
from pandas_extensions import *

class TestPandasExtensions(unittest.TestCase):
  def test_series_one_hot_encode(self):
    s = pd.Series(['a', 'b', 'c'])
    s2 = s.one_hot_encode()
    self.assertTrue(np.array_equal(s2.values, np.array([
      [1., 0., 0.], 
      [0., 1., 0.], 
      [0., 0., 1.]], 'object')))

  def test_series_binning(self):
    s = pd.Series([1., 2., 3.])    
    s2 = s.bin(2)
    self.assertTrue(np.array_equal(s2.values, np.array(
      ['(0.998, 2]', '(0.998, 2]', '(2, 3]'], 'object')))

  def test_categoricals(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'n_1': [1., 2., 3.]})
    self.assertTrue(['c_1'] == df.categoricals())

  def test_appending_sparseness_2(self):
    df = pd.DataFrame({'n_1': [1., 2., 3.], 'n_2': [1., 2., 3.]}).to_sparse(fill_value=0)
    df['n_3'] = pd.Series([0, 0, 1]).to_sparse(fill_value=0)

    self.assertTrue(np.array_equal(df.values, np.array([
      [1., 1., 0.], 
      [2., 2., 0.], 
      [3., 3., 1.]], 'object')))

  def test_one_hot_encode(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'n_1': [1., 2., 3.]})
    df = df.one_hot_encode().toarray()    
    self.assertTrue((3, 4) == df.shape)
    np.testing.assert_array_equal(df, [
      [1., 0., 0., 1.], 
      [0., 1., 0., 2.], 
      [0., 0., 1., 3.]])

  def test_one_hot_encode_with_multiple_columns(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'n_1': [1., 2., 3.], 'c_3': ['d', 'e', 'f']})
    df = df.one_hot_encode().toarray()
    self.assertTrue((3, 7) == df.shape)
    np.testing.assert_array_equal(df, [
      [1., 0., 0., 1., 0., 0., 1.], 
      [0., 1., 0., 0., 1., 0., 2.], 
      [0., 0., 1., 0., 0., 1., 3.]])

  def test_binning(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'n_1': [1., 2., 3.]})    
    df.bin(2)
    self.assertTrue((3, 3) == df.shape)
    self.assertTrue(np.array_equal(df.values, np.array([
      ['a', 1., '(0.998, 2]'], 
      ['b', 2., '(0.998, 2]'], 
      ['c', 3., '(2, 3]']], 'object')))

  def test_binning_with_remove(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'n_1': [1., 2., 3.]})    
    df.bin(2, True)
    self.assertTrue((3, 2) == df.shape)
    self.assertTrue(np.array_equal(df.values, np.array([
      ['a', '(0.998, 2]'], 
      ['b', '(0.998, 2]'], 
      ['c', '(2, 3]']], 'object')))

  def test_remove_categoricals(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'n_1': [1., 2., 3.]})    
    df.remove(categoricals=True)
    self.assertTrue(['n_1'] == df.columns)

  def test_remove_numericals(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'n_1': [1., 2., 3.]})    
    df.remove(numericals=True)
    self.assertTrue(['c_1'] == df.columns)

  def test_remove_binaries(self):
    df = pd.DataFrame({'b_1':['a', 'b', 'c'], 'd_1': [1., 2., 3.]})    
    df.remove(binaries=True)
    self.assertTrue(['d_1'] == df.columns)

  def test_remove_dates(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'd_1': [1., 2., 3.]})    
    df.remove(dates=True)
    self.assertTrue(['c_1'] == df.columns)

  def test_engineer_concat(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'c_2': ['d', 'e', 'f']})    
    df.engineer('c_1(:)c_2')
    self.assertTrue(np.array_equal(df['c_1(:)c_2'].values, 
      np.array(['ad', 'be', 'cf'], 'object')))

  def test_engineer_concat_3_cols(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'c_2': ['d', 'e', 'f'], 'c_3': ['h', 'i', 'j']})    
    df.engineer('c_3(:)c_1(:)c_2')
    self.assertTrue(np.array_equal(df['c_3(:)c_1(:)c_2'].values, 
      np.array(['had', 'ibe', 'jcf'], 'object')))

  def test_engineer_concat_with_numerical_col(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'c_2': [1, 2, 3]})    
    df.engineer('c_1(:)c_2')
    self.assertTrue(np.array_equal(df['c_1(:)c_2'].values, 
      np.array(['a1', 'b2', 'c3'], 'object')))

  def test_engineer_concat_with_numerical_col_3_cols(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'n_2': [1, 2, 3], 'n_3': [4, 5, 6]})    
    df.engineer('n_3(:)c_1(:)n_2')
    self.assertTrue(np.array_equal(df['c_n_3(:)c_1(:)n_2'].values, 
      np.array(['4a1', '5b2', '6c3'], 'object')))

  def test_engineer_multiplication(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'n_2': [1, 2, 3], 'n_3': [4, 5, 6], 'n_4': [7, 8, 9]})    
    df.engineer('n_2(*)n_3')
    self.assertTrue(np.array_equal(df['n_2(*)n_3'].values, 
      np.array([4, 10, 18], long)))

  def test_engineer_multiplication_3_cols(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'n_2': [1, 2, 3], 'n_3': [4, 5, 6], 'n_4': [7, 8, 9]})    
    df.engineer('n_2(*)n_3(*)n_4')
    self.assertTrue(np.array_equal(df['n_2(*)n_3(*)n_4'].values, 
      np.array([4*7, 80, 18*9], long)))

  def test_square_on_whole_data_frame(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'n_2': [1, 2, 3], 'n_3': [4, 5, 6], 'n_4': [7, 8, 9]})    
    df.engineer('(^2)')
    self.assertTrue(np.array_equal(df.values, 
      np.array([
        ['a', 1, 4, 7, 1*1, 4*4, 7*7],
        ['b', 2, 5, 8, 2*2, 5*5, 8*8],
        ['c', 3, 6, 9, 3*3, 6*6, 9*9],
        ], 'object')))

  def test_square_on_cols(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'n_2': [1, 2, 3], 'n_3': [4, 5, 6], 'n_4': [7, 8, 9]})    
    df.engineer('n_3(^2)')
    self.assertTrue(np.array_equal(df.values, 
      np.array([
        ['a', 1, 4, 7, 4*4],
        ['b', 2, 5, 8, 5*5],
        ['c', 3, 6, 9, 6*6],
        ], 'object')))

  def test_log_on_whole_data_frame(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'n_2': [1, 2, 3], 'n_3': [4, 5, 6], 'n_4': [7, 8, 9]})    
    df.engineer('(lg)')
    self.assertTrue(np.array_equal(df.values, 
      np.array([
        ['a', 1, 4, 7, math.log(1), math.log(4), math.log(7)],
        ['b', 2, 5, 8, math.log(2), math.log(5), math.log(8)],
        ['c', 3, 6, 9, math.log(3), math.log(6), math.log(9)],
        ], 'object')))

  def test_log_on_cols(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'n_2': [1, 2, 3], 'n_3': [4, 5, 6], 'n_4': [7, 8, 9]})    
    df.engineer('n_3(lg)')
    self.assertTrue(np.array_equal(df.values, 
      np.array([
        ['a', 1, 4, 7, math.log(4)],
        ['b', 2, 5, 8, math.log(5)],
        ['c', 3, 6, 9, math.log(6)],
        ], 'object')))

  def test_combinations(self):
    df = pd.DataFrame({'c_1':[], 'c_2':[], 'c_3':[], 
      'n_1': [], 'n_2': [], 'n_3': []})    
    self.assertTrue([('c_1', 'c_2'), ('c_1', 'c_3'), ('c_2', 'c_3')] ==
      df.combinations(2, categoricals=True))

    combs = [('c_1', 'c_2'), ('c_1', 'c_3'), ('c_1', 'n_1'), 
      ('c_1', 'n_2'), ('c_1', 'n_3'), ('c_2', 'c_3'), ('c_2', 'n_1'),
      ('c_2', 'n_2'), ('c_2', 'n_3'), ('c_3', 'n_1'), ('c_3', 'n_2'), 
      ('c_3', 'n_3'), ('n_1', 'n_2'), ('n_1', 'n_3'), ('n_2', 'n_3')]
    self.assertTrue(combs == df.combinations(2, categoricals=True, numericals=True))

  def test_chaining(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'c_2':['d', 'e', 'f'], 
      'n_2': [1, 2, 3], 'n_3': [4, 5, 6], 'n_4': [7, 8, 9]})    
    df.\
      engineer('c_1(:)c_2').\
      engineer('c_1(:)n_2').\
      engineer('n_2(*)n_3').\
      engineer('n_2(lg)').\
      engineer('n_3(^2)')

    self.assertTrue(np.array_equal(df.values, 
      np.array([
        ['a', 'd', 1, 4, 7, 'ad', 'a1', 4, math.log(1), 4*4],
        ['b', 'e', 2, 5, 8, 'be', 'b2', 10, math.log(2), 5*5],
        ['c', 'f', 3, 6, 9, 'cf', 'c3', 18, math.log(3), 6*6]
        ], 'object')))

  def test_scale(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'c_2':['d', 'e', 'f'], 
      'n_2': [1., 2., 3.], 'n_3': [4., 5., 6.], 'n_4': [7., 8., 9.]})
    df.scale()
    self.assertTrue(np.array_equal(df.values, 
      np.array([
        ['a', 'd', -1.224744871391589, -1.224744871391589, -1.224744871391589],
        ['b', 'e', 0, 0, 0],
        ['c', 'f', 1.224744871391589, 1.224744871391589, 1.224744871391589]
        ], 'object')))

  def test_scale_with_min_max(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c'], 'c_2':['d', 'e', 'f'], 
      'n_2': [1., 2., 3.], 'n_3': [4., 5., 6.], 'n_4': [7., 8., 9.]})        
    df.scale((0., 2.))
    self.assertTrue(np.array_equal(df.values, 
      np.array([
        ['a', 'd', 0, 0, 0],
        ['b', 'e', 1, 1, 1],
        ['c', 'f', 2, 2, 2]
        ], 'object')))

  def test_missing_vals_in_categoricals_mode(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c', 'a', np.nan], 
      'n_2': [1, 2, 3, 1, np.nan]})        
    df.missing(categorical_fill='mode')
    self.assertEqual('a', df['c_1'][4])

  def test_missing_vals_in_categoricals_constant(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c', 'a', np.nan], 
      'n_2': [1, 2, 3, 1, np.nan]})        
    df.missing(categorical_fill='f')
    self.assertEqual('f', df['c_1'][4])

  def test_missing_vals_in_numericals_mode(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c', 'a', np.nan], 
      'n_2': [1, 2, 3, 1, np.nan]})              
    df.missing(numerical_fill='mode')
    self.assertEqual(1, df['n_2'][4])

  def test_missing_vals_in_numericals_mean(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c', 'a', np.nan], 
      'n_2': [1, 2, 3, 1, np.nan]})              
    df.missing(numerical_fill='mean')
    self.assertEqual(1.75, df['n_2'][4])

  def test_missing_vals_in_numericals_max(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c', 'a', np.nan], 
      'n_2': [1, 2, 3, 1, np.nan]})              
    df.missing(numerical_fill='max')
    self.assertEqual(3, df['n_2'][4])

  def test_missing_vals_in_numericals_min(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c', 'a', np.nan], 
      'n_2': [1, 2, 3, 1, np.nan]})              
    df.missing(numerical_fill='min')
    self.assertEqual(1, df['n_2'][4])

  def test_missing_vals_in_numericals_median(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c', 'a', np.nan], 
      'n_2': [1, 2, 3, 1, np.nan]})              
    df.missing(numerical_fill='median')
    self.assertEqual(1.5, df['n_2'][4])

  def test_missing_vals_in_numericals_constant(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c', 'a', np.nan], 
      'n_2': [1, 2, 3, 1, np.nan]})              
    df.missing(numerical_fill=-10)
    self.assertEqual(-10, df['n_2'][4])

  def test_outliers(self):
    df = pd.DataFrame({'n_1':np.random.normal(size=200)})
    min_1, max_1 = df.n_1.min(), df.n_1.max()
    df.outliers(2)
    min_2, max_2 = df.n_1.min(), df.n_1.max()
    self.assertTrue(min_1 < min_2)
    self.assertTrue(max_1 > max_2)

  def test_categorical_outliers(self):
    cols = ['a', 'b', 'c', 'd'] * 100000
    cols = cols + ['f', 'g'] * 10000
    df = pd.DataFrame({'c_1': cols})
    df.categorical_outliers(0.1)
    np.testing.assert_array_equal(
      ['a', 'b', 'c', 'd', 'a', 'b', 'c', 'd'],
      df.c_1.values[:8])
    self.assertEqual('others', df.c_1.values[-1])

  def test_append_right(self):
    df1 = pd.DataFrame({'c_1':['a', 'b'], 
      'n_1': [1, 2]})              
    df2 = pd.DataFrame({'c_2':['c', 'd'], 
      'n_2': [3, 4]})              
    df1 = df1.append_right(df2)
    self.assertTrue(np.array_equal(df1.values, 
      np.array([
        ['a', 1, 'c', 3],
        ['b', 2, 'd', 4]
        ], 'object')))

  def test_append_bottom(self):
    df1 = pd.DataFrame({'c_1':['a', 'b'], 
      'n_1': [1, 2]})              
    df2 = pd.DataFrame({'c_1':['c', 'd'], 
      'n_1': [3, 4]})              
    df1 = df1.append_bottom(df2)
    self.assertTrue(np.array_equal(df1.values, 
      np.array([
        ['a', 1],
        ['b', 2],
        ['c', 3],
        ['d', 4]
        ], 'object')))

  def test_shuffle(self):
    df = pd.DataFrame({'c_1':['a', 'b', 'c', 'd', 'e', 'f', 'g'], 'n_1': [1, 2, 3, 4, 5, 6, 7]})
    y = pd.Series([1L, 2L, 3L, 4L, 5L, 6L, 7L])
    df2, y2 = df.shuffle(y)

    # Originals did not change
    np.testing.assert_array_equal(df.values, np.array([['a', 1L], ['b', 2L], ['c', 3L], ['d', 4L], ['e', 5L], ['f', 6L], ['g', 7L]], dtype='object'))
    np.testing.assert_array_equal(y.values, [1, 2, 3, 4, 5, 6, 7])
    # Changed
    self.assertFalse(np.array_equal(df2.values, np.array([['a', 1L], ['b', 2L], ['c', 3L], ['d', 4L], ['e', 5L], ['f', 6L], ['g', 7L]], dtype='object')))
    self.assertFalse(np.array_equal(y2.values, np.array([1, 2, 3, 4, 5, 6, 7])))

    self.assertEqual((7, 2), df2.shape)
    self.assertEqual(7, len(y2))
    for i, v in enumerate(y2):
      self.assertEqual(v, df2.n_1[i])


  def test_describe_data(self):
    pass

if __name__ == '__main__':
  unittest.main()
