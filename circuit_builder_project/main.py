from circuit_builder_project.circuit_builder import CircuitBuilder

if __name__ == "__main__":
    print("=== Построитель электрических цепей ===\n")
    print("Введите описание цепи (элементы через точку с запятой):")
    print("Формат: [id][узел1][узел2] - Тип = значение")
    print("Пример: 114 - ИН и = 2; 212 - R2 = 2; 324 - L3 = 2")
    user_input = input("\nВаш ввод: ")

    circuit_user = CircuitBuilder()
    if circuit_user.parse_circuit_string(user_input):
        circuit_user.draw_circuit()
    else:
        print("Ошибка при обработке ввода!")