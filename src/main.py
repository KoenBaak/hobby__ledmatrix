from driver import MatrixDriver, Color

driver = MatrixDriver()
colors = driver.color_manager
all_blue = [[Color(red=0, green=1, blue=1)] * driver.n_rows] * driver.n_cols
driver.show_frame(all_blue)
