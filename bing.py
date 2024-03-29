from os import system, listdir, remove

cookie = '19TMNdh9_tPCmYpIna-bVF9S9zx_sr6y7zgfy3v3dbdkAUmhDLSk_ukXkX95-WsK1R1wpfWouxLxIspjI6brnEhhrgQuE0Z1PDub5gGQFZWaua7Oiq7OTE4UowzGUCQ_nc6jVB2kFYH5twNgJCCazu0qcWvyXDA6-vJw8sT470loS485liHVc-1-Har2Rik1ZoWEekvogu-PC2mkE8Rn0UQ'

def Generate_Image(prompt):
    try:
        # Delete previously generated images
        for file in listdir('output'):
            remove(f'output/{file}')

        command = f'python -m BingImageCreator --prompt "{prompt}" -U "{cookie}"'
        print("Executing command:", command)
        system(command)
        output_files = listdir('output')
        print("Generated images:", output_files)
        return output_files
    except Exception as e:
        print("An error occurred:", e)

# try:
#     Generate_Image('girl doing coding')
# except Exception as e:
#     print("An error occurred while generating images:", e)

