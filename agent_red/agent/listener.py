"""
Description
=====
class Listener is defined here to managing session between an agent master and agent slaves.
Further, communication between them is performed through this class.
class Listener is a singleton class because an agent master requires only one listener.
"""

import sys, threading, time, socket, constant
from singleton import Singleton

class Listener(Singleton):
    """
    Managing session between an agent master and agent slaves.
    """

    __stop = False
    """
    A flag to terminate listening thread.
    """

    __thread = None
    """
    An instance for inner thread.
    Inner thread should be instanciated only one. Thus, a private member for this instance is defined.
    """

    __table = {}
    """
    Table for session instances.
    """

    __id = 1
    """
    Counter for allocating an unique ID for table records.
    """

    def __accept(self, sock):
        """
        Accept requests from red team agents.
        If a stop flag is turned on, socket and session table will be destroyed at the end of this function.

        :param sock: a socket of an agent master.
        """
        while not Listener.__stop:
            try:
                conn, clientaddr = sock.accept()
            except socket.timeout:
                continue

            self.__update_state(clientaddr[0], conn)
            print ("[SERVER] Connection Established (" + clientaddr[0] + ")")

        sock.close()
        for e in Listener.__table:
            Listener.__table[e]["sock"].close()
        Listener.__table.clear()

    def __request_state(self, sock):
        """
        Send a message to update a status of a given socket.
        Request will be sent to a related agent slave, and the agent slave will response with its current state.

        :param sock: socket to be updated

        :return state: a current state of related agent slave.
        """
        try:
            state = self.__send_using_socket(sock, "cat " + constant.TEMPORARY_FILE_SHELL + "\n")
        except Error as e:
            state = None
        return state

    def __new_session_record(self, address, state, sock):
        """
        Register new session record in the session table.

        :param address: an address of a session to be reigstered.
        :param state: a state of a current session.
        :param sock: a session to be updated.
        """

        Listener.__table[str(Listener.__id)] = {
            "address" : address,
            "state" : state,
            "sock" : sock
        }
        Listener.__id += 1

    def __update_session_record(self, id, state, sock):
        """
        Update a session record in the session table.

        :param id: a session table id to be updated.
        :param state: a state of a current session.
        :param sock: a session to be updated.
        """
        if sock.fileno() != Listener.__table[id]["sock"].fileno():
            Listener.__table[id]["sock"].close()
            Listener.__table[id]["sock"] = sock
        Listener.__table[id]["state"] = state

    def __update_state(self, address, sock):
        """
        Update a state of a session.

        :param address: session address to be updated.
        :param sock: session socket to be updated.
        """
        state = self.__request_state(sock)
        if state is None:
            return

        record = self.get_session(address)

        if record is None:
            self.__new_session_record(address, state, sock)
            print ("[LISTENER] Connection Registered")
        else:
            self.__update_session_record(record, state, sock)
            print ("[LISTENER] Connection Updated")

    def __send_using_socket(self, sock, msg):
        """
        Send message to a socket.

        :param sock: socket to send a message.
        :param msg: message to be sent.

        :return string: a message to be sent.
        """
        sock.send(msg.encode())
        return str(self.__recv_using_socket(sock)).strip()

    def __recv_using_socket(self, sock):
        """
        Receive message from a socket.

        :param sock: socket to receive message.

        :return string: a response message.
        """
        data = ""
        sock.settimeout(2)
        try:
            while True:
                part = sock.recv(1024)
                part = part.decode()
                data += part
                if len(part) < 1024:
                    break
        except socket.timeout:
            pass
        return data

    def __str__(self):
        msg = "Listener ======\n"
        cnt = 1
        for e in Listener.__table:
            msg += "[" + str(cnt) + "] " + str(Listener.__table[e]) + "\n"
            cnt += 1
        msg += "==============="
        return msg

    def stop(self):
        """
        Stopping a listener, which means a termination of inner thread.
        This function only sends a signal to inner thread, then inner thread will terminate itself.
        """

        print ("[Listener] Start stopping server")
        Listener.__stop = True
        print ("[Listener] Server stopped")

    def work(self, ip, port):
        """
        Start a listener.

        :param ip: IP address for a listener socket.
        :param port: port address for a listener socket.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:
            sock.bind((ip, port))
        except socket.error:
            print ("Address already in use (" + ip + ":" + port + ")")
            return

        sock.listen(1)
        sock.settimeout(1)
        Listener.__thread = threading.Thread(target = self.__accept, args=(sock, ))
        Listener.__thread.start()

    def get_session(self, address):
        """
        Get session ID by using its address

        :param address: an address of a session.

        :return session: None if no session exist with a given address.
        """
        for e1 in Listener.__table:
            t_value = Listener.__table[e1]
            t_address = t_value["address"]

            if address == t_address:
                return e1

        return None

    def update_state_as_address(self, address):
        """
        The same functuality as update_state.

        :param address: address to be updated.

        """
        record = self.get_session(address)
        sock = Listener.__table[record]["sock"]
        state = self.__request_state(sock)
        Listener.__table[record]["state"] = state

    def get_state(self, address):
        """
        Get table record ID of an given address

        :param address: session address that is wanted to know its ID.

        :return int: a session table ID. None if there is no related record in the session table.
        """
        record = self.get_session(address)
        if record is None:
            return None

        return Listener.__table[record]["state"]

    def send(self, address, msg):
        """
        Send a message to a session that is related to a given address.
        This message is working synchronously that means it waits for a response from a remote host.

        :param address: An address to send message.
        :param msg: A messsage to be sent.

        :return string: A response message.
        """

        print ("[LISTENER] Attempt to send message [" + msg + "] to (" + address + ")")
        record = self.get_session(address)
        if record == None:
            return None
        sock = Listener.__table[record]["sock"]
        return self.__send_using_socket(sock, msg)

    def send_only(self, address, msg):
        """
        Send a message to a session that is related to a given address.
        This message is working ansynchronously that means it does not recieve any message.

        :param address: An address to send message.
        :param msg: A messsage to be sent.

        :return string: A response message.
        """
        print ("[LISTENER] Attempt to send message [" + msg + "] to (" + address + ")")
        record = self.get_session(address)
        if record == None:
            return
        sock = Listener.__table[record]["sock"]
        sock.send(msg.encode())
