from django.http import JsonResponse
import requests
import random

def get_data(request):
    url_param = request.GET.getlist('url')
    
    # Initialize lists to store prime and Fibonacci numbers
    prime_numbers = prime(request)['prime_numbers']
    fibonacci_sequence = fibo(request)['fibonacci_sequence']
    
    # Find numbers that are both prime and in the Fibonacci sequence
    common_numbers = list(set(prime_numbers) & set(fibonacci_sequence))
    
    result = {'common_numbers': common_numbers}
    
    for url in url_param:
        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                result[url] = data
            else:
                result[url] = {'error': 'Failed to fetch data from the URL'}

        except requests.exceptions.RequestException as e:
            result[url] = {'error': str(e)}
    
    return JsonResponse(result)

def odd(request):
    odd_list = [x for x in range(1, 51) if x % 2 != 0]
    return JsonResponse({'odd_numbers': odd_list})

def rand(request):
    lower_limit = 1
    upper_limit = 100
    array_size = 10
    random_integers = [random.randint(lower_limit, upper_limit) for _ in range(array_size)]
    return JsonResponse({'random_numbers': random_integers})

def fibo(request):
    fibonacci_sequence = [0, 1]
    
    while True:
        next_fib = fibonacci_sequence[-1] + fibonacci_sequence[-2]
        if next_fib <= 50:
            fibonacci_sequence.append(next_fib)
        else:
            break
    
    return JsonResponse({'fibonacci_sequence': fibonacci_sequence})

def prime(request):
    prime = [True for _ in range(51)]
    prime[0] = prime[1] = False
    
    p = 2
    while p * p <= 50:
        if prime[p]:
            for i in range(p * p, 50 + 1, p):
                prime[i] = False
        p += 1

    primes = [i for i in range(2, 50 + 1) if prime[i]]
    return JsonResponse({'prime_numbers': primes})
