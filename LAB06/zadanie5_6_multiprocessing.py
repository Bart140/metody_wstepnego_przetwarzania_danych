import os
import pandas as pd
from datetime import datetime
from itertools import repeat
from multiprocessing import Pool, cpu_count
from filesplit.split import Split


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), 'data')


def sizeof_fmt(num, suffix="B"):
    for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"


def count_time(func):
    def wrapper(*args, **kwargs):
        start = datetime.now()
        result = func(*args, **kwargs)
        elapsed = datetime.now() - start
        print(f"Czas wykonania {func.__name__}: {elapsed}")
        return result
    return wrapper


def apply_args_and_kwargs(func, args, kwargs):
    return func(*args, **kwargs)


def starmap_with_kwargs(pool, func, args_iter, kwargs_iter):
    args_for_starmap = zip(repeat(func), args_iter, kwargs_iter)
    return pool.starmap(apply_args_and_kwargs, args_for_starmap)


def split_file(filepath, chunksize, destination):
    os.makedirs(destination, exist_ok=True)
    split = Split(filepath, destination)
    split.bylinecount(linecount=chunksize, includeheader=True)


def load_files_mp(directory, n_processes):
    files = [[f"{directory}/{f}"] for f in sorted(os.listdir(directory)) if f.endswith(".csv")]
    kwargs_list = [{'on_bad_lines': "skip"} for _ in range(len(files))]
    pool = Pool(processes=n_processes)
    results = starmap_with_kwargs(pool, pd.read_csv, files, kwargs_list)
    pool.close()
    pool.join()
    return pd.concat(results, ignore_index=True)


def sum_likes_from_file(filepath):
    df = pd.read_csv(filepath, on_bad_lines='skip')
    return df['likes'].sum()


if __name__ == '__main__':
    csv_path = os.path.join(BASE_DIR, 'instagram_data.csv')
    split_dir = os.path.join(BASE_DIR, 'data_split')
    n_cores = cpu_count()
    print(f"Liczba rdzeni CPU: {n_cores}")

    if not os.path.exists(csv_path):
        print("Plik instagram_data.csv nie istnieje, tworzę z plików parquet...")
        df1 = pd.read_parquet(os.path.join(DATA_DIR, '0000.parquet'))
        df2 = pd.read_parquet(os.path.join(DATA_DIR, '0001.parquet'))
        df_all = pd.concat([df1, df2], ignore_index=True)
        del df1, df2
        df_all.to_csv(csv_path, header=True, index=False)
        del df_all
        print(f"Zapisano: {csv_path}")

    print("\nZADANIE 5 - Multiprocessing")

    if os.path.exists(split_dir):
        for f in os.listdir(split_dir):
            os.remove(os.path.join(split_dir, f))
    split_file(csv_path, 500_000, split_dir)
    n_files = len([f for f in os.listdir(split_dir) if f.endswith('.csv')])
    print(f"Podzielono plik na {n_files} części")

    procs_1 = max(1, n_cores - 2)
    procs_2 = max(1, (n_cores - 2) * 2)

    start = datetime.now()
    df_mp1 = load_files_mp(split_dir, procs_1)
    t_mp1 = datetime.now() - start
    print(f"Multiprocessing ({procs_1} procesów): {t_mp1}")
    del df_mp1

    try:
        start = datetime.now()
        df_mp2 = load_files_mp(split_dir, procs_2)
        t_mp2 = datetime.now() - start
        print(f"Multiprocessing ({procs_2} procesów): {t_mp2}")
        del df_mp2
    except Exception as e:
        print(f"Błąd przy {procs_2} procesach: {type(e).__name__}: {e}")

    print("\nZADANIE 6 - Sekwencyjne vs równoległe sumowanie likes")


    csv_files = sorted([
        os.path.join(split_dir, f) for f in os.listdir(split_dir)
        if f.endswith('.csv')
    ])
    print(f"Liczba plików: {len(csv_files)}")

    start = datetime.now()
    total_likes_seq = 0
    for fpath in csv_files:
        df_chunk = pd.read_csv(fpath, on_bad_lines='skip')
        total_likes_seq += df_chunk['likes'].sum()
    t_seq = datetime.now() - start
    print(f"Suma likes (sekwencyjnie): {total_likes_seq:,}")
    print(f"Czas: {t_seq}")

    n_procs = max(1, cpu_count() - 2)
    start = datetime.now()
    with Pool(processes=n_procs) as pool:
        partial_sums = pool.map(sum_likes_from_file, csv_files)
    total_likes_par = sum(partial_sums)
    t_par = datetime.now() - start
    print(f"Suma likes (równolegle): {total_likes_par:,}")
    print(f"Czas: {t_par}")
    print(f"Przyspieszenie: {t_seq.total_seconds() / t_par.total_seconds():.2f}x")
