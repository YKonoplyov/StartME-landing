import React, { useState, useEffect } from 'react';
import { useTable, usePagination, useFilters } from 'react-table';
import Modal from '@/components/main/modal/Modal';
import Images from '@/image/image';

function MainTable() {
    const [data, setData] = useState([]);
    const [filteredData, setFilteredData] = useState([]);
    const [filterInput, setFilterInput] = useState('');
    const [selectedUser, setSelectedUser] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [filterInputVisible, setFilterInputVisible] = useState(false);
    const [newUserData, setNewUserData] = useState({
        name: '',
        nicknameOld: '',
        discipline: '',
        fullName: '',
        description: '',
        amount: '',
        gipsyteam: ''
    });

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch('/records.json');
                if (!response.ok) {
                    throw new Error('Failed to fetch data');
                }
                const jsonData = await response.json();
                setData(Array.isArray(jsonData.items) ? jsonData.items : []);
            } catch (error) {
                console.error('Error fetching data: ', error);
            }
        };
        fetchData();
    }, []);

    useEffect(() => {
        setFilteredData(
            data.filter(item =>
                Object.values(item).some(value =>
                    value && value.toString().toLowerCase().includes(filterInput.toLowerCase())
                )
            )
        );
    }, [data, filterInput]);

    const openModal = () => {
        setIsModalOpen(true);
    };

    const openViewModal = (user) => {
        setSelectedUser(user);
    };

    const closeViewModal = () => {
        setSelectedUser(null);
    };

    const handleChange = e => {
        const { name, value } = e.target;
        setNewUserData(prevData => ({
            ...prevData,
            [name]: value
        }));
    };

    const handleSubmit = async () => {
        try {
            const createdAt = new Date().toISOString()
            const userDataWithTimestamp = {
                ...newUserData,
                createdAt: createdAt
            }
            const response = await fetch('/addUser', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userDataWithTimestamp)
            });
            if (!response.ok) {
                throw new Error('Failed to add user');
            }
            setIsModalOpen(false);
        } catch (error) {
            console.error('Error adding user: ', error);
        }
    };

    const columns = React.useMemo(
        () => [
            {
                Header: 'Фонд',
                accessor: 'found.name',
            },
            {
                Header: 'Создано',
                accessor: row => {
                    const createdAt = new Date(row.created_at);
                    return `${createdAt.getFullYear()}-${String(createdAt.getMonth() + 1).padStart(2, '0')}-${String(createdAt.getDate()).padStart(2, '0')}`;
                },
            },
            {
                Header: 'Обновлено',
                accessor: row => {
                    const updatedAt = new Date(row.updated_at);
                    return `${updatedAt.getFullYear()}-${String(updatedAt.getMonth() + 1).padStart(2, '0')}-${String(updatedAt.getDate()).padStart(2, '0')}`;
                },
            },
            {
                Header: 'Ники',
                accessor: 'nicknameOld',
                Cell: ({ value }) => <div className="truncate">{value}</div>,
            },
            {
                Header: 'Дисциплина',
                accessor: row => (row.nicknames && row.nicknames.length > 0) ? row.nicknames[0].room_name : '',
            },
            {
                Header: 'ФИО',
                accessor: row => {
                    const { first_name = '', last_name = '', middlename = '' } = row;
                    return `${first_name}${last_name ? ' ' + last_name : ''}${middlename ? ' ' + middlename : ''}`;
                },
            },
            {
                Header: 'Описание',
                accessor: 'description',
                Cell: ({ value }) => <div className="truncate">{value}</div>,
            },
            {
                Header: 'Ущерб',
                accessor: 'amount',
            },
            {
                Header: 'Gipsy team',
                accessor: 'gipsyteam',
            },
        ],
        []
    );

    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        page,
        prepareRow,
        gotoPage,
        pageCount,
        state: { pageIndex },
        canPreviousPage,
        canNextPage,
        previousPage,
        nextPage,
    } = useTable(
        {
            columns,
            data: filteredData,
            initialState: { pageIndex: 0 },
        },
        useFilters,
        usePagination
    );

    const inputLabels = {
        name: "Фонд",
        createdAt: "Создано",
        updatedAt: "Обновлено",
        nicknameOld: "Ники",
        discipline: "Дисциплина",
        fullName: "ФИО",
        description: "Описание",
        amount: "Ущерб",
        gipsyteam: "Gipsy team"
    };

    const toggleFilterInput = () => {
        setFilterInputVisible(!filterInputVisible);
        setFilterInput('');
    };

    const ModalContent = (
        <Modal active={isModalOpen} setActive={setIsModalOpen}>
            <button className="modal__btn-close" onClick={() => setIsModalOpen(false)} />
            <div className="table__modal-title">
                Добавить пользователя
            </div>
            <form className="table__modal-form-wrap" onSubmit={handleSubmit} method="POST">
                {Object.keys(newUserData).map(key => (
                    <div className="table__modal-row" key={key}>
                        <label className="table__modal-cell-title" htmlFor={key}>{inputLabels[key]}</label>
                        <input
                            className="table__modal-cell"
                            id={key}
                            type="text"
                            name={key}
                            value={newUserData[key]}
                            onChange={handleChange}
                            autoComplete="off"
                        />
                    </div>
                ))}
                <button className="btn-hover table__btn" type="submit">
                    Добавить
                </button>
            </form>
        </Modal>
    );

    const ViewModalContent = selectedUser && (
        <Modal active={selectedUser !== null} setActive={closeViewModal}>
            <button className="modal__btn-close" onClick={closeViewModal} />
            <div className="table__modal-title">
                Информация о пользователе
            </div>
            <div className="table__modal-form-wrap">
                {columns.slice(0, -1).map(column => (
                    <div className="table__modal-row" key={column.accessor}>
                        <div className="table__modal-cell-title">
                            {column.Header}
                        </div>
                        <div className="table__modal-cell">
                            {selectedUser && column.accessor(selectedUser)}
                        </div>
                    </div>
                ))}
            </div>
        </Modal>
    );

    const PreviousPageButton = ({ onClick, disabled }) => (
        <button className={`pagination__btn ${disabled ? 'disabled' : ''}`} onClick={onClick} disabled={disabled}>
            <img src={Images.arrow} alt="arrow" />
        </button>
    );

    const NextPageButton = ({ onClick, disabled }) => (
        <button className={`pagination__btn ${disabled ? 'disabled' : ''}`} onClick={onClick} disabled={disabled}>
            <img src={Images.arrow} alt="arrow" />
        </button>
    );

    const PageButtons = (
        <div className="pagination__wrap">
            <PreviousPageButton onClick={previousPage} disabled={!canPreviousPage} />
            {Array.from({ length: pageCount }, (_, i) => (
                <button
                    key={i}
                    onClick={() => gotoPage(i)}
                    className={`pagination__btn-op ${pageIndex === i ? 'active' : ''}`}
                >
                    {i + 1}
                </button>
            ))}
            <NextPageButton onClick={nextPage} disabled={!canNextPage}/>
        </div>
    );

    return (
        <main id="main" className="main">
            <div className="table__top-wrap">
                <div></div>
                <div className="table__top">
                    <input
                        className={filterInputVisible ? "input__search" : "input__search input__search-op"}
                        value={filterInput}
                        onChange={e => setFilterInput(e.target.value)}
                        placeholder="Поиск..."
                    />
                    <button className="table__top-btn" onClick={toggleFilterInput}>
                        <img src={Images.search} alt="search"/>
                    </button>
                    <button className="table__top-btn" onClick={openModal}>
                        <img src={Images.add} alt="add"/>
                    </button>
                </div>
            </div>
            <table className="table" {...getTableProps()}>
                <thead className="table__header-wrap">
                {headerGroups.map(headerGroup => (
                    <tr className="table__header" {...headerGroup.getHeaderGroupProps()}>
                        {headerGroup.headers.map(column => (
                            <th className="table__headers" {...column.getHeaderProps()}>
                                {column.render('Header')}
                            </th>
                        ))}
                    </tr>
                ))}
                </thead>
                <tbody className="table__body-wrap" {...getTableBodyProps()}>
                {page.map(row => {
                    prepareRow(row);
                    return (
                        <tr className="table__body" {...row.getRowProps()} onClick={() => openViewModal(row.original)}>
                            {row.cells.map((cell, index) => (
                                <td key={index} className="table__body-cell truncate">{cell.render('Cell')}</td>
                            ))}
                        </tr>
                    );
                })}
                </tbody>
            </table>
            {PageButtons}
            {ModalContent}
            {ViewModalContent}
        </main>
    );
}

export default MainTable;