import re
import subprocess
import ipaddress

# 文件配置
ips = "Fission_ip.txt"
ip2cc = "Fission_ip2cc.txt"

# 使用mmdblookup查找ASN信息
def get_asn(ip):
    try:
        result = subprocess.run(["mmdblookup", "--file", "GeoLite2-ASN.mmdb", "--ip", ip, "autonomous_system_number"], capture_output=True, text=True)
        asn = re.search(r'\d+', result.stdout)
        if asn:
            return asn.group()
        else:
            return None
    except Exception as e:
        print(f"Error looking up ASN for IP {ip}: {e}")
        return None

# 使用mmdblookup查找国家代码信息
def get_country_code(ip):
    try:
        result = subprocess.run(["mmdblookup", "--file", "GeoLite2-Country.mmdb", "--ip", ip, "country", "iso_code"], capture_output=True, text=True)
        country_code = re.search(r'"([A-Z]{2})"', result.stdout)
        if country_code:
            return country_code.group(1)
        else:
            return None
    except Exception as e:
        print(f"Error looking up country code for IP {ip}: {e}")
        return None

# 分类IP地址并生成结果文件
def classify_ip_addresses(input_file, output_file):
    try:
        with open(input_file, "r") as infile, open(output_file, "w") as outfile:
            for line in infile:
                ip = line.strip()
                if ip:
                    try:
                        ip_obj = ipaddress.ip_address(ip)
                        if ip_obj.is_global:
                            country_code = get_country_code(ip)
                            if country_code:
                                outfile.write(f"{ip}#{country_code}\n")
                            else:
                                print(f"Country code lookup failed for IP: {ip}")
                    except ValueError:
                        print(f"Invalid IP address: {ip}")
    except Exception as e:
        print(f"Error processing IP addresses: {e}")

# 主函数
def main():
    classify_ip_addresses(ips, ip2cc)
    print("IP地址分类并生成国家代码完成")

# 程序入口
if __name__ == '__main__':
    main()
