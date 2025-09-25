def count_numbers_with_digit_sum(target_sum, num_digits):
    # Cria uma tabela para armazenar os resultados parciais
    dp = [[0] * (target_sum + 1) for _ in range(num_digits + 1)]
    dp[0][0] = 1  # Base case: existe uma maneira de obter a soma 0 com 0 dígitos

    for digit_count in range(1, num_digits + 1):
        for sum_val in range(target_sum + 1):
            for digit in range(10):
                if sum_val >= digit:
                    dp[digit_count][sum_val] += dp[digit_count - 1][sum_val - digit]
    
    return dp[num_digits][target_sum]

# Definindo a soma alvo (19) e o número máximo de dígitos (6)
target_sum = 19
num_digits = 6

print("Número de inteiros positivos com soma de dígitos igual a 19:", count_numbers_with_digit_sum(target_sum, num_digits))
