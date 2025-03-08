# Automating CML Topology Creation
The Python code that I provided is essentially a topology generator for Cisco Modeling Labs (CML), which is a network simulation platform used for designing, testing, and validating network configurations. Let me break down why this Python code is useful and why you might need it for CML:

## Installation

Provide installation instructions and usage details here.

## Ingredients

  * [CML](https://software.cisco.com/download/home/286193282/type/286326381/release/CML-Free)
  * [vmWare Workstation](https://support.broadcom.com/group/ecx/productdownloads?subfamily=VMware+Workstation+Pro)
  * 
## Prerequisites

A\. Add the Cisco IOSv,IOSvL2, IOL and IOLL2 to the CML .

<pre>
$ <b>vagrant box list | grep iosv</b>
cisco-iosv        vios-adventerprisek9-m.spa.159-3.m6.qcow2
cisco-iosvl2      vios_l2-adventerprisek9-m.ssa.high_iron_20200929.qcow2
cisco-iol         x86_64_crb_linux-adventerprisek9-ms.iol
cisco-iol2        x86_64_crb_linux_l2-adventerprisek9-ms.iol
</pre>

# 1. Automating Topology Creation
CML allows you to create network topologies manually using its graphical user interface (GUI). However, for large or complex topologies, manually adding devices, connections, and configurations can be time-consuming and error-prone. This Python script automates the process by:

1 - Reading a simple text file (input.txt) that defines the connections between devices.
2 - Generating a YAML file (Router_Configuration.yaml) that CML can import to create the topology automatically.

This saves a lot of time, especially when dealing with large-scale networks.

# Example Use Case
Imagine you are designing a network with 10 routers and 5 switches, all interconnected in a specific way. Instead of manually adding each device and connection in CML:

You define the connections in input.txt:

r1 e0/0 r2 e0/0
r1 e0/1 r3 e0/0
s1 e0/0 r4 e0/1

You run the Python script, which generates a YAML file (Router_Configuration.yaml).

You import the YAML file into CML, and the topology is created automatically.

This process is much faster and less error-prone than doing it manually.
