def compute():
    result_text.delete(1.0, 'end')  # Clear previous results
    input_file_a = "Tema3/input_files/sum/a.txt"
    input_file_b = "Tema3/input_files/sum/b.txt"
    input_file_aplusb = "Tema3/input_files/sum/aplusb.txt"

    if format_var.get() == "DS":
        success, result = compute_sum_ds(input_file_a, input_file_b, input_file_aplusb)
    else:
        success, result = compute_sum_crs(input_file_a, input_file_b, input_file_aplusb)

    result_text.insert('end', f"Format: {format_var.get()}\n\n")
    if success:
        result_text.insert('end', "Sum Result:\n")
        result_text.insert('end', result['result'])
        result_text.insert('end', f"\nVerification: {'Success' if result['verification'] else 'Failed'}")
    else:
        result_text.insert('end', f"Error: {result}") 