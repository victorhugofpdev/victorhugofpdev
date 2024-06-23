import subprocess
import re
import matplotlib.pyplot as plt

def run_simulation(command, output_file):
    with open(output_file, 'w') as file:
        result = subprocess.run(command, shell=True, text=True, stdout=subprocess.PIPE)
        file.write(result.stdout)

def parse_output(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    job_times = {}
    for line in lines:
        match = re.search(r'--> JOB (\d) DONE at time (\d+)', line)
        if match:
            job_id = int(match.group(1))
            finish_time = int(match.group(2))
            job_times[job_id] = finish_time
    
    return job_times

def compute_fairness(job_times):
    times = list(job_times.values())
    fairness = min(times) / max(times) if max(times) > 0 else 1
    return fairness

# Step 1: Simulations with 3 jobs and random seeds
for seed in [1, 2, 3]:
    command = f"python lottery.py -s {seed} -j 3 -c"
    output_file = f"output_seed_{seed}.txt"
    run_simulation(command, output_file)

# Step 2: Two specific jobs
command = "python lottery.py -l 10:1,10:100 -c"
run_simulation(command, "output_two_specific_jobs.txt")

# Step 3: Two jobs of length 100 and equal tickets
command = "python lottery.py -l 100:100,100:100 -c"
run_simulation(command, "output_equal_length_and_tickets.txt")

# Step 4: Varying quantum sizes
for quantum in [50, 100, 200]:
    command = f"python lottery.py -l 10:1,10:100 -q {quantum} -c"
    output_file = f"output_quantum_{quantum}.txt"
    run_simulation(command, output_file)

# Step 5: Collect data for fairness graph
job_lengths = [10, 100, 1000]
fairness_data = []

for length in job_lengths:
    command = f"python lottery.py -l {length}:100,{length}:100 -c"
    output_file = f"output_{length}.txt"
    run_simulation(command, output_file)
    job_times = parse_output(output_file)
    fairness = compute_fairness(job_times)
    fairness_data.append((length, fairness))

# Plot and save the graph
run_lengths, fairness_values = zip(*fairness_data)
plt.plot(run_lengths, fairness_values, marker='o')
plt.xlabel('Job Length')
plt.ylabel('Fairness')
plt.title('Lottery Scheduler Fairness Study')
plt.xscale('log')
plt.yscale('linear')
plt.savefig('fairness_study.png')

print("Simulations completed and results saved to text files. Fairness graph saved as 'fairness_study.png'.")
