import interface as inter

print(inter.retrieve_id(10))
print(inter.retrieve_many(10, 18))

inter.insert_row("JOHN A", "HIMMLER", 1488)

inter.edit_row(17, "pay", 1488)
inter.edit_row(17, "first", "KLAUS")

inter.delete_row(17)
