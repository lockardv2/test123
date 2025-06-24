from pymodbus.client.sync import ModbusTcpClient
#from pymodbus.client import ModbusTcpClient
import time, sys, traceback
import sqlite3

# SQLite DB 설정
DB_NAME = '/home/sch/devlopment/server/dashboard/db.sqlite3'  # DB 경로 수정

# 데이터 저장
def save_to_db(plc_id_id, slave_id, slave_vendor, slave_product, slave_version, product_id, slave_temp, slave_status):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO dashboard_core_slavedevice (plc_id_id, slave_id, slave_vendor, slave_product, slave_version, product_id, slave_temp, slave_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', 
                       (plc_id_id, slave_id, slave_vendor, slave_product, slave_version, product_id, slave_temp, slave_status))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()

# 최신 데이터 조회
def get_latest_data(plc_id_id, product_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT slave_temp FROM dashboard_core_slavedevice WHERE plc_id_id = ? AND product_id = ? ORDER BY id DESC LIMIT 1', (plc_id_id, product_id))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

# product_id 존재 여부 확인
def product_id_exists(plc_id_id, product_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM dashboard_core_slavedevice WHERE plc_id_id = ? AND product_id = ?', (plc_id_id, product_id))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

# Modbus 데이터 읽기 (TCP)
def read_registers(client, slave_id, register_ranges):
    slave_vendor, slave_product, slave_version, product_id, slave_temp = "", "", "", "", ""

    for register_address in range(max(end for _, end, _ in register_ranges) + 1):
        result = client.read_holding_registers(register_address, 1, unit=slave_id)
        if not result.isError():
            value = result.registers[0]
            for start, end, var_name in register_ranges:
                if start <= register_address <= end:
                    if var_name == "slave_vendor":
                        slave_vendor += chr(value)
                    elif var_name == "slave_product":
                        slave_product += chr(value)
                    elif var_name == "slave_version":
                        slave_version += chr(value)
                    elif var_name == "product_id":
                        product_id += chr(value)
                    elif var_name == "slave_temp":
                        slave_temp += chr(value)
                    break
        else:
            print(f"Error reading register {register_address} for slave {slave_id}")

    return slave_id, slave_vendor.strip(), slave_product.strip(), slave_version.strip(), product_id.strip(), slave_temp.strip()

def read_modbus(modbus_ip, modbus_port, slave_id, register_ranges):
    client = ModbusTcpClient(modbus_ip, modbus_port)
    connection = client.connect()

    if connection:
        result = read_registers(client, slave_id, register_ranges)
        client.close()
        return result
    else:
        print(f"Failed to connect to Modbus server at {ip}:{port}")
        return None

# 주기적으로 데이터 수집
def main():
    modbus_ip = "192.168.81.128"  # PLC 시뮬레이터의 IP 주소
    modbus_port = 502  # Modbus TCP 포트
    plc_id_id = "1"  # PLC ID 정의

    register_ranges = {
        1: [(0, 3, "slave_vendor"), (4, 18, "slave_product"), (19, 22, "slave_version"), (23, 29, "product_id"), (30, 33, "slave_temp")],
        2: [(0, 6, "slave_vendor"), (7, 16, "slave_product"), (17, 20, "slave_version"), (21, 26, "product_id"), (27, 30, "slave_temp")],
        3: [(0, 17, "slave_vendor"), (18, 29, "slave_product"), (30, 33, "slave_version"), (34, 42, "product_id"), (43, 46, "slave_temp")],
        4: [(0, 5, "slave_vendor"), (6, 14, "slave_product"), (15, 17, "slave_version"), (18, 23, "product_id"), (24, 27, "slave_temp")]
    }

    while True:
        try:
            for slave_id in range(1, 5):
                result = read_modbus(modbus_ip, modbus_port, slave_id, register_ranges[slave_id])
                if result:
                    slave_id, slave_vendor, slave_product, slave_version, product_id, slave_temp = result
                    print(f"Slave ID: {slave_id}, Vendor: {slave_vendor}, Product: {slave_product}, Version: {slave_version}, Product ID: {product_id}, Temp: {slave_temp}")

                    slave_status = True if slave_id in [1, 2, 3] else False
                    
                    # product_id 존재 여부 체크
                    if not product_id_exists(plc_id_id, product_id):
                        latest_value = get_latest_data(plc_id_id, product_id)
                        if latest_value is None or latest_value != slave_temp:
                            save_to_db(plc_id_id, slave_id, slave_vendor, slave_product, slave_version, product_id, slave_temp, slave_status)

            time.sleep(3)
        except (KeyboardInterrupt, SystemExit):
            print('Turn off')
            sys.exit(0)
        except Exception as e:
            print(traceback.format_exc())
            sys.exit(0)


if __name__ == '__main__':
    main()
