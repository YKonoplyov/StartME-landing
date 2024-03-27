import React, { useState, useEffect } from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import 'swiper/swiper-bundle.css';

const Funds = ({ items, filterParams }) => {
    const [filteredItems, setFilteredItems] = useState(items);
    const [initialFilters, setInitialFilters] = useState({});

    useEffect(() => {
        applyFilters(initialFilters);
    }, [items, initialFilters]);

    const applyFilters = (filters) => {
        let filtered = items;
        for (const param in filters) {
            if (filters[param]) {
                filtered = filtered.filter(item => item[param] === filters[param]);
            }
        }
        setFilteredItems(filtered);
    };

    const onFilterChange = (param, value) => {
        const filters = { ...initialFilters, [param]: value };
        setInitialFilters(filters);
    };

    useEffect(() => {
        if (filterParams.length > 0) {
            const firstParam = filterParams[0].name;
            const initialValue = filterParams[0].options[0];
            const filters = { [firstParam]: initialValue };
            setInitialFilters(filters);
        }
    }, [filterParams]);

    return (
        <section id="Funds" className="funds__wrap">
            <Filter
                filterParams={filterParams}
                onChange={onFilterChange}
                initialFilters={initialFilters}
            />
            <Swiper
                pagination={{ clickable: true }}
                spaceBetween={30}
                slidesPerView={3}
            >
                {filteredItems.map(item => (
                    <SwiperSlide key={item.id}>
                        <div className="swiper-slide">
                            <img src={item.image} alt={item.title} />
                            <h3>{item.title}</h3>
                        </div>
                    </SwiperSlide>
                ))}
            </Swiper>
        </section>
    );
};

const Filter = ({ filterParams, onChange, initialFilters }) => {
    const handleFilterChange = (param, value) => {
        onChange(param, value);
    };

    return (
        <div className="filter-container">
            {filterParams.map(param => (
                <div key={Math.random()}>
                    <div className="filter-buttons">
                        {param.options.map(option => (
                            <button
                                key={option}
                                onClick={() => handleFilterChange(param.name, option)}
                                className={initialFilters[param.name] === option ? "active" : ""}
                            >
                                {option}
                            </button>
                        ))}
                    </div>
                </div>
            ))}
        </div>
    );
};

export default Funds;
