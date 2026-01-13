import os
import heapq
import random
import glob

class PolyphaseSort:
    def __init__(self, filename: str, chunk_size: int = 10):
        self.filename   = filename
        self.chunk_size = chunk_size
        self.run_files  = []  # Список всех созданных серий
        
        # Три "ленты". В реальности это были бы физические устройства/файлы.
        # Здесь мы храним списки имен файлов-серий, лежащих на этой "ленте".
        self.tapes = [[], [], []] 

    def create_initial_runs(self):
        """
        Фаза 0: Читаем исходный файл кусками, сортируем в памяти 
        и сохраняем как временные файлы (серии).
        """
        with open(self.filename, 'r') as f:
            chunk = []
            run_count = 0
            for line in f:
                chunk.append(int(line.strip()))
                if len(chunk) >= self.chunk_size:
                    self._save_run(chunk, run_count)
                    chunk = []
                    run_count += 1
            
            # Сохраняем остаток
            if chunk:
                self._save_run(chunk, run_count)

    def _save_run(self, data, index):
        """Сортирует данные и пишет во временный файл"""
        data.sort()
        run_name = f"run_{index}.tmp"
        with open(run_name, 'w') as f:
            for num in data:
                f.write(f"{num}\n")
        self.run_files.append(run_name)

    def get_fib_distribution(self, n_runs):
        """
        Рассчитывает идеальное распределение Фибоначчи.
        Нам нужно найти два последовательных числа Фибоначчи F(k) и F(k-1),
        сумма которых >= количеству реальных серий.
        """
        f0, f1 = 0, 1
        while f0 + f1 < n_runs:
            f0, f1 = f1, f0 + f1
        return f1, f0  # Возвращаем (большее, меньшее)

    def distribute_runs(self):
        """
        Фаза 1: Распределение.
        Раскладываем серии по Ленте 0 и Ленте 1 согласно числам Фибоначчи.
        Лента 2 остается пустой (приемник).
        """
        total_runs = len(self.run_files)
        target_t1, target_t2 = self.get_fib_distribution(total_runs)
        
        needed_dummy = (target_t1 + target_t2) - total_runs
        print(f"Всего серий: {total_runs}. Цель (Fib): {target_t1} и {target_t2}. Фиктивных: {needed_dummy}")

        # Распределяем реальные файлы
        current_run_idx = 0
        
        # Заполняем Ленту 0
        for _ in range(target_t1):
            if current_run_idx < total_runs:
                self.tapes[0].append(self.run_files[current_run_idx])
                current_run_idx += 1
            else:
                self.tapes[0].append(None) # Dummy run

        # Заполняем Ленту 1
        for _ in range(target_t2):
            if current_run_idx < total_runs:
                self.tapes[1].append(self.run_files[current_run_idx])
                current_run_idx += 1
            else:
                self.tapes[1].append(None) # Dummy run

        # Лента 2 пуста
        self.tapes[2] = []

    def merge_phase(self):
        """
        Фаза 2: Многофазное слияние.
        """
        # Индексы лент: source1, source2, dest
        t_idx = [0, 1, 2] 
        phase = 1

        while True:
            # Определяем, сколько серий сливать (по самой короткой ленте)
            # Игнорируем пустые ленты при подсчете (лента-приемник всегда пуста в начале шага)
            lens = [len(self.tapes[i]) for i in t_idx]
            
            # Если на двух лентах пусто (или 0 и 1 серия), а на третьей 1 серия - мы закончили
            total_remaining = sum(lens)
            if total_remaining == 1:
                final_tape = [i for i in t_idx if len(self.tapes[i]) == 1][0]
                return self.tapes[final_tape][0]

            # Находим две входные ленты (те, что не пустые)
            # В классической схеме одна всегда пустая (приемник), две полные.
            # Но после ротации индексы меняются.
            # Логика: Входные ленты те, где есть серии. Приемник - пустая.
            input_indices = [i for i in t_idx if len(self.tapes[i]) > 0]
            dest_index = [i for i in t_idx if len(self.tapes[i]) == 0][0]

            # Количество слияний на этом этапе = количеству серий на меньшей из входных лент
            merge_count = min(len(self.tapes[i]) for i in input_indices)
            
            print(f"\n--- Фаза {phase} ---")
            print(f"Ленты (кол-во серий): {lens}")
            print(f"Слияние {merge_count} серий с {input_indices} на ленту {dest_index}")

            for _ in range(merge_count):
                # Берем по одной серии с каждой входной ленты
                run_a = self.tapes[input_indices[0]].pop(0)
                run_b = self.tapes[input_indices[1]].pop(0)
                
                new_run_name = self._merge_two_runs(run_a, run_b)
                self.tapes[dest_index].append(new_run_name)

            phase += 1

    def _merge_two_runs(self, file_a, file_b):
        """
        Сливает два файла (или файл и Dummy) в один новый.
        """
        # Логика Dummy runs:
        # Если оба None -> результат None (Dummy)
        # Если один None -> результат копия второго (просто переносим)
        # Если оба файлы -> честное слияние
        
        if file_a is None and file_b is None:
            return None
        
        if file_a is None:
            return file_b # Или переименовать/копировать для чистоты, но здесь просто вернем
        if file_b is None:
            return file_a

        # Реальное слияние двух файлов
        output_filename = f"merged_{random.randint(1000,9999)}.tmp"
        
        with open(file_a, 'r') as fa, open(file_b, 'r') as fb, open(output_filename, 'w') as fout:
            # Генераторы, читающие числа из файлов
            iter_a = (int(line) for line in fa)
            iter_b = (int(line) for line in fb)
            
            # heapq.merge делает всю грязную работу по слиянию сортированных потоков
            for num in heapq.merge(iter_a, iter_b):
                fout.write(f"{num}\n")

            # def get_next_val(f):
            #     line = f.readline()
            #     if not line:
            #         return None
            #     return int(line.strip())
            
            # val_a = get_next_val(fa)
            # val_b = get_next_val(fb)

            # while (val_a is not None) and (val_b is not None):
            #     if val_a < val_b:
            #         fout.write(f"{val_a}\n")
            #         val_a = get_next_val(fa)
            #     else:
            #         fout.write(f"{val_b}\n")
            #         val_b = get_next_val(fb)
            
            # while val_a:
            #     fout.write(f"{val_a}\n")
            #     val_a = get_next_val(fa)
            
            # while val_b:
            #     fout.write(f"{val_b}\n")
            #     val_b = get_next_val(fb)

            # Cleanup
            # os.remove(file_a)
            # os.remove(file_b)

        
        # Удаляем старые куски (опционально, чтобы не засорять диск)
        # os.remove(file_a) # Можно раскомментировать
        # os.remove(file_b)
        
        return output_filename

    def cleanup(self):
        """Удаляет все .tmp файлы"""
        for f in glob.glob("*.tmp"):
            try:
                os.remove(f)
            except:
                pass

# --- Запуск ---

# 1. Создадим тестовый файл
input_file = "input_data.txt"
with open(input_file, "w") as f:
    # 55 случайных чисел
    nums = [random.randint(1, 1000) for _ in range(55)]
    f.write("\n".join(map(str, nums)))

print("Данные сгенерированы.")

sorter = PolyphaseSort(input_file, chunk_size=5) # Маленький размер чанка, чтобы было много серий

try:
    # Шаг 1: Создаем серии
    sorter.create_initial_runs()
    
    # Шаг 2: Распределяем по Фибоначчи
    sorter.distribute_runs()
    
    # Шаг 3: Сливаем
    result_file = sorter.merge_phase()
    
    print(f"\nСортировка завершена! Итоговый файл: {result_file}")
    
    # Проверка результата
    if result_file:
        with open(result_file, 'r') as f:
            res_nums = [int(line) for line in f]
        print(f"Первые 10 чисел результата: {res_nums[:10]}")
        print(f"Отсортировано верно? {res_nums == sorted(nums)}")

finally:
    # Очистка
    sorter.cleanup() # Раскомментируйте, чтобы удалить мусор
    pass