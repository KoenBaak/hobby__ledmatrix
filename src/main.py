from driver import MatrixDriver, Color

driver = MatrixDriver(n_color_bits=8)
colors = driver.color_manager
all_blue = [[colors.relative(red=1.0, green=.4, blue=.6)] * driver.n_rows] * driver.n_cols
print(all_blue[0][0])
driver.show_frame(all_blue)
