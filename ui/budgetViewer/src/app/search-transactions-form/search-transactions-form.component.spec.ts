import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchTransactionsFormComponent } from './search-transactions-form.component';

describe('SearchTransactionsFormComponent', () => {
  let component: SearchTransactionsFormComponent;
  let fixture: ComponentFixture<SearchTransactionsFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SearchTransactionsFormComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SearchTransactionsFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
