from driver import MatrixDriver

driver = MatrixDriver()
colors = driver.color_manager
all_blue = [[colors.relative(.2, .3, .2)] * driver.n_cols] * driver.n_rows
driver.show_frame(all_blue)
