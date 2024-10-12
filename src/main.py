from driver import MatrixDriver

driver = MatrixDriver()
colors = driver.color_manager
all_blue = [[colors.blue()] * driver.n_cols] * driver.n_rows
driver.show_frame(all_blue)
