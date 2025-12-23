import matplotlib.pyplot as plt

# Membuat Bar Chart dari hasil grouping tadi
group['gaji'].plot(kind='bar')

plt.title('Rata-rata Gaji per Departemen')
plt.ylabel('Gaji')
plt.show()

# ================================================================================
